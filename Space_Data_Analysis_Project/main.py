import pandas as pd
import plotly.express as px
import tkinter as tk


df = pd.read_csv("mission_launches.csv", index_col=False)  # Loading and cleaning Data for usage
df = df.loc[:, ~df.columns.str.contains('^Unnamed') & (df.columns != '')]
df['Date_clean'] = df['Date'].astype(str).str.replace(r'(\d{4}).*', r'\1', regex=True).str.strip()
df['Date_parsed'] = pd.to_datetime(df['Date_clean'], errors='coerce')

df['Year'] = df['Date_parsed'].dt.year

df['Month'] = df['Date_parsed'].dt.month_name()

df['Price'] = pd.to_numeric(df['Price'], errors='coerce')


#   Functions that will be used in a TkInter GUI
def plot_sunburst():
    top_orgs = (
        df.groupby(['Year', 'Organisation'])
        .size()
        .reset_index(name='Count')
        .sort_values(['Year', 'Count'], ascending=[True, False])
        .groupby('Year')
        .first()
        .reset_index()
    )

    fig = px.sunburst(
        top_orgs,
        path=['Year', 'Organisation'],
        values='Count',
        hover_data={'Count': True, 'Year': True, 'Organisation': True},
    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{customdata[1]}<br>' +
                      '<b>Organisation:</b> %{customdata[2]}<br>' +
                      '<b>Count:</b> %{value:,}'
    )

    fig.update_layout(
        title="Top Organisation per Year",
        width=800,
        height=800,
        margin=dict(t=50, l=0, r=0, b=0)
    )

    fig.show()


def plot_avg_cost():
    df_cost = df.dropna(subset=['Price', 'Year'])
    avg_cost = df_cost.groupby('Year')['Price'].mean().reset_index()

    fig = px.line(
        avg_cost,
        x='Year',
        y='Price',
        markers=True,
        title='Average Mission Cost per Year',
        labels={'Price': 'Avg Cost (Million USD)', 'Year': 'Year'}
    )
    fig.update_traces(mode='lines+markers')
    fig.update_layout(width=800, height=500)
    fig.show()


month_counts = df['Month'].value_counts().reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])


def plot_popular_months():
    # Plot bar chart with Plotly Express
    fig = px.bar(
        month_counts,
        x=month_counts.index,
        y=month_counts.values,
        labels={'x': 'Month', 'y': 'Number of Missions'},
        title='Number of Missions per Month (All Years)'
    )
    fig.show()


def plot_mission_status_per_year():
    df['Year'] = df['Year'].astype(int)

    statuses = ['Success', 'Prelaunch Failure', 'Partial Failure', 'Failure']
    total_counts = df.groupby('Year').size().reset_index(name='Total')

    dfs = []
    for status in statuses:
        filtered = df[df['Mission_Status'] == status]
        counts = filtered.groupby('Year').size().reset_index(name='Count')
        merged = counts.merge(total_counts, on='Year', how='right').fillna(0)
        merged['Percentage'] = (merged['Count'] / merged['Total']) * 100
        merged['Status'] = status
        dfs.append(merged[['Year', 'Percentage', 'Status']])

    combined = pd.concat(dfs)

    fig = px.line(
        combined,
        x='Year',
        y='Percentage',
        color='Status',
        title='Mission Status Percentages per Year',
        labels={
            'Year': 'Year',
            'Percentage': 'Percentage (%)',
            'Status': 'Mission Status'
        }
    )

    fig.update_traces(
        hovertemplate='Year: %{x}<br>Status: %{legendgroup}<br>Percentage: %{y:.1f}%<extra></extra>'
    )

    fig.show()


#  TkInter Gui
root = tk.Tk()
root.title("Data manipulation project")
root.geometry("300x200")

btn1 = tk.Button(root, text="Show Sunburst", command=plot_sunburst, font=("Arial", 12), width=25)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Show Avg Cost per Year", command=plot_avg_cost, font=("Arial", 12), width=25)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Show Popular Months", command=plot_popular_months, font=("Arial", 12), width=25)
btn3.pack(pady=10)

btn4 = tk.Button(root, text="Show Mission Status Trend", command=plot_mission_status_per_year, font=("Arial", 12), width=25)
btn4.pack(pady=10)

root.mainloop()

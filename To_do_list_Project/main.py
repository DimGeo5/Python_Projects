from flask import Flask,  render_template_string, request, redirect, url_for, session
from datetime import datetime, timedelta
import hashlib
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
TASKS_DATA_FILE = 'tasks_db.json'


@app.template_filter('to_datetime')   # a custom filter named to_datetime that converts strings to datetime objects.
def to_datetime(value, date_format='%Y-%m-%d'):  # it is used for due dates of tasks
    return datetime.strptime(value, date_format)


def load_users_db():  # exception in order to open json file with registered users, if already exists
    try:
        with open('users_db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_users_db():  # function that adds users, when called
    with open('users_db.json', 'w') as f:
        json.dump(users_db, f)


def load_tasks_db():
    try:
        with open(TASKS_DATA_FILE, 'r') as f:   # same as users dictionary
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_tasks_db():        # same as users dictionary
    with open(TASKS_DATA_FILE, 'w') as f:
        json.dump(tasks, f)


users_db = load_users_db()   # previous functions called when the app starts
tasks = load_tasks_db()


@app.route('/')     # home page before login or register
def home_page():
    return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome</title>
                <style>
                    body, h1, h2 {
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }
                    header {
                        background-color: #4682B4; 
                        color: white;                     
                        padding: 20px;
                    }
                    body {
                        background-color: #f4f4f4;
                        padding: 20px;
                    }
                    form {
                        max-width: 400px;
                        margin: 0 auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    input {
                        padding: 10px;
                        margin: 10px 0;
                        width: 100%;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                    }
                    button {
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        
                    }
                    button:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
               <header>
                    <h1>Welcome to My To-Do List App</h1>
               </header>
               <h2>Please choose one of the options below:</h2>
               <div>
                    <a href="/register"><button>Register</button></a>
                    <a href="/login"><button>Login</button></a>
               </div>
            </body>
            </html>
            """)


@app.route('/register', methods=['GET', 'POST'])  # register page, checks if username already exists as well
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db:
            return render_template_string("""
                                 <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Login</title>
                        <style>
                            body, h1, h2 {
                                margin: 0;
                                padding: 0;
                                font-family: Arial, sans-serif;
                                text-align: center;
                            }
                            header {
                                background-color: #4682B4; 
                                color: white;                        
                                padding: 20px;
                            }
                            body {
                                background-color: #f4f4f4;
                                padding: 20px;
                            }
                            form {
                                max-width: 400px;
                                margin: 0 auto;
                                background-color: #fff;
                                padding: 20px;
                                border-radius: 8px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            }
                            input {
                                padding: 10px;
                                margin: 10px 0;
                                width: 100%;
                                border-radius: 5px;
                                border: 1px solid #ccc;
                            }
                            button {
                                padding: 10px 20px;
                                background-color: #4CAF50;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                width: 100%;
                            }
                            button:hover {
                                background-color: #45a049;
                            }
                        </style>
                    </head>
                    <body>
                        <header>
                            <h1>Username already exists, please choose a different one.</h1>
                        </header>
                        <form method="POST">
                            <label for="username">Username:</label>
                            <input type="text" name="username" required><br><br>
                            <label for="password">Password:</label>
                            <input type="password" name="password" required><br><br>
                            <button type="submit">Login</button>
                        </form>
                    </body>
                    </html>
                    """)

        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # hashed module used for more secure passwords
        users_db[username] = hashed_password                            # maybe a little too much but I liked it when
                                                                        # read about it, and I wanted to use it
        save_users_db()

        return redirect(url_for('login'))

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Register</title>
            <style>
                body, h1, h2 {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                header {
                    background-color: #4682B4; 
                    color: white;                        
                    padding: 20px;
                }
                body {
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                form {
                    max-width: 400px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                input {
                    padding: 10px;
                    margin: 10px 0;
                    width: 100%;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
           <header>
                <h1>Register</h1>
           </header>
           <form method="POST">
                <label for="username">Username:</label>
                <input type="text" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" name="password" required><br><br>
                <button type="submit">Register</button>
        </form>

            <br>
            <a href="{{ url_for('login') }}">Already have an account? Login</a>
        </body>
        </html>
        """)


@app.route('/login', methods=['GET', 'POST'])   # login page,checks if username or password is wrong
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if users_db.get(username) == hashed_password:
            session['username'] = username
            return redirect(url_for('home_page_logged_in'))
        else:
            return render_template_string("""
                     <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
            <style>
                body, h1, h2 {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                header {
                    background-color: #4682B4; 
                    color: white;                        
                    padding: 20px;
                }
                body {
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                form {
                    max-width: 400px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                input {
                    padding: 10px;
                    margin: 10px 0;
                    width: 100%;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Invalid username or password</h1>
                <h2>Please try again<h2>
            </header>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" name="password" required><br><br>
                <button type="submit">Login</button>
            </form>
            <br>
            <a href="{{ url_for('register') }}">Don't have an account? Register</a>
        </body>
        </html>
        """)

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
            <style>
                body, h1, h2 {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                header {
                    background-color: #4682B4; 
                    color: white;                        
                    padding: 20px;
                }
                body {
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                form {
                    max-width: 400px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                input {
                    padding: 10px;
                    margin: 10px 0;
                    width: 100%;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Login</h1>
            </header>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" name="password" required><br><br>
                <button type="submit">Login</button>
            </form>
            <br>
            <a href="{{ url_for('register') }}">Don't have an account? Register</a>
        </body>
        </html>
        """)


@app.route('/home', methods=['GET', 'POST'])  # home page if user is logged in
def home_page_logged_in():
    global tasks

    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    today_date = datetime.today().date()       # saves the today date so later a user will not be able to use past dates
    max_date = today_date + timedelta(days=365)   # or dates after one year (as max date)

    today_date_str = today_date.strftime('%Y-%m-%d')
    max_date_str = max_date.strftime('%Y-%m-%d')

    if request.method == 'POST':
        task_name = request.form['task']
        due_date = request.form['due_date']

        if task_name:
            if username not in tasks:
                tasks[username] = []

            tasks[username].append({
                'task': task_name,
                'due_date': due_date,
                'completed': False,
            })

            save_tasks_db()    # function called, to save user's tasks

    home_page_layout = """
    <!DOCTYPE html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>To-Do List</title>
            <style>
                body, h1, h2, h3 {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                }
                header {
                    background-color: #4682B4; 
                    color: white;               
                    text-align: center;         
                    padding: 20px;
                }
                body {
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                form {
                    max-width: 400px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                input {
                    padding: 10px;
                    margin: 10px 0;
                    width: 100%;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                }
                button:hover {
                    background-color: #45a049;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    background-color: #fff;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                a {
                    text-decoration: none;
                    color: red;
                    margin-left: 10px;
                }
        </style>
        </head>
        <body>
             <header>
                <h1>Welcome, {{ username }} to your To-Do List app! Add your tasks below!</h1>
             </header>
             <form method="POST">
                    <input type="text" name="task" placeholder="Add here your task" required>
                    <input type="date" name="due_date"
                            min="{{ today_date }}" 
                            max="{{ max_date }}">
                    <button type="submit">Add Task</button>
             </form>
             <h3>Your Tasks:</h3>
             <ul>
                {% for task in tasks %}
                    <li>
                        {{ task['task'] }} - Due: {{ task['due_date'] }}
                        {% if not task['completed'] %}
                            <a href="{{ url_for('complete_task', task_id=loop.index0) }}" style="color: \
                                                                        #4CAF50">Complete</a>
                            <a href="{{ url_for('delete_task', task_id=loop.index0) }}">Delete</a>
                        {% else %}
                            <span>
                                {% set due_date_obj = task['due_date'] | to_datetime('%Y-%m-%d') %}
                                {% set completed_date_obj = task['completed_at'] | to_datetime('%Y-%m-%d %H:%M:%S') %}
                                {% if completed_date_obj > due_date_obj %}
                                    <span style="color: orange;">Completed</span>
                                    {{ task['completed_at'] }}
                                {% else %}
                                    <span style="color: green;">Completed</span>
                                    {{ task['completed_at'] }}
                                {% endif %}
                            </span>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
            
            <a href="{{ url_for('logout') }}">Logout</a>
        </body>
    </html>
    """
    user_tasks = tasks.get(username, [])
    return render_template_string(home_page_layout, tasks=user_tasks, username=username,
                                  today_date=today_date_str, max_date=max_date_str)


@app.route('/complete_task/<int:task_id>')    # This  decorator used for completed tasks
def complete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    if username in tasks and 0 <= task_id < len(tasks[username]):
        task = tasks[username][task_id]
        task['completed'] = True
        task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_tasks_db()
    return redirect(url_for('home_page_logged_in'))


@app.route('/delete_task/<int:task_id>')   # this is used for deleting tasks
def delete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    if username in tasks and 0 <= task_id < len(tasks[username]):
        tasks[username].pop(task_id)
    return redirect(url_for('home_page_logged_in'))


@app.route('/logout')   # and this is used for logging out
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

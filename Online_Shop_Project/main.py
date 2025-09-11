import csv
from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Products of the e-shop
products = [
    {'id': 1, 'name': 'T-shirt', 'description': 'Comfortable cotton t-shirt', 'price': 20.0},
    {'id': 2, 'name': 'Jeans', 'description': 'Stylish denim jeans', 'price': 40.0},
    {'id': 3, 'name': 'Sneakers', 'description': 'Comfy running sneakers', 'price': 60.0},
]

# A csv that stores users and passwords
USERS_CSV = 'users.csv'

# A function to find
def read_users_from_csv():
    users = {}
    try:
        with open(USERS_CSV, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    users[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return users


# A function to write users to CSV
def write_user_to_csv(username, password):
    with open(USERS_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])


current_user = None


@app.route('/')
def index():
    page = '''
    <html>
    <head>
        <title>Simple eCommerce</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; background-color: #f8f9fa; }
            .navbar { background-color: #343a40; }
            .navbar a { color: #fff; }
            .navbar .navbar-brand { font-weight: bold; }
            .product-card { margin-bottom: 20px; }
            .footer { background-color: #343a40; color: white; padding: 10px 0; text-align: center; position: fixed; bottom: 0; width: 100%; }
            .container { max-width: 1200px; }
            .card-title { font-size: 1.25rem; }
        </style>
    </head>
    <body>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#">eCommerce</a>
            <div class="d-flex">
                {% if current_user %}
                    <span class="navbar-text text-light">Hello, {{ current_user }}! 
                    <a href="{{ url_for('logout') }}" class="btn btn-danger btn-sm ml-2">Logout</a>
                    <a href="{{ url_for('view_cart') }}" class="btn btn-info btn-sm ml-2">Go to Cart</a></span>
                {% else %}
                    <a href="{{ url_for('login') }}" class="btn btn-primary btn-sm ml-2">Login</a> 
                    <a href="{{ url_for('register') }}" class="btn btn-success btn-sm ml-2">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <!-- Product List -->
    <div class="container mt-5">
        <h2 class="mb-4">Our Products</h2>
        <div class="row">
        {% for product in products %}
            <div class="col-md-4">
                <div class="card product-card">
                    <img src="https://via.placeholder.com/150" class="card-img-top" alt="{{ product.name }}">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text">{{ product.description }}</p>
                        <p><strong>${{ product.price }}</strong></p>
                        {% if current_user %}
                            <a href="{{ url_for('add_to_cart', product_id=product.id) }}" class="btn btn-primary">Add to Cart</a>
                        {% else %}
                            <a href="{{ url_for('login') }}" class="btn btn-primary">Login to Add</a>
                        {% endif %}
                    </div>
                </div>
            </div>
        {% endfor %}
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <p>&copy; 2025 eCommerce Store</p>
    </div>

    </body>
    </html>
    '''
    return render_template_string(page, products=products, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Read users from CSV and validate login
        users = read_users_from_csv()
        if username in users and users[username] == password:
            current_user = username
            return redirect(url_for('index'))
        else:
            return "<div class='alert alert-danger'>Invalid credentials</div>", 401

    page = '''
    <html>
    <head>
        <title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .container { max-width: 500px; margin-top: 50px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="mb-4">Login</h2>
            <form method="POST">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
            <p class="mt-3">Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(page)


@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Checking if the username exists
        users = read_users_from_csv()
        if username not in users:
            # Add user to CSV if the username is available
            write_user_to_csv(username, password)
            return redirect(url_for('login'))
        else:
            return "<div class='alert alert-danger'>Username already exists</div>", 400

    page = '''
    <html>
    <head>
        <title>Register</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .container { max-width: 500px; margin-top: 50px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="mb-4">Register</h2>
            <form method="POST">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success">Register</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(page)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/cart')
def view_cart():
    cart_items = [product for product in products if product['id'] in session.get('cart', [])]
    total = sum(item['price'] for item in cart_items)

    page = '''
    <html>
    <head>
        <title>Your Cart</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h2>Your Shopping Cart</h2>
            {% if cart_items %}
                <ul class="list-group">
                {% for item in cart_items %}
                    <li class="list-group-item">
                        {{ item.name }} - ${{ item.price }}
                        <a href="{{ url_for('remove_from_cart', product_id=item.id) }}" class="btn btn-danger btn-sm float-end">Remove</a>
                    </li>
                {% endfor %}
                </ul>
                <p class="mt-3"><strong>Total: ${{ total }}</strong></p>
                <a href="{{ url_for('checkout') }}" class="btn btn-success">Proceed to Checkout</a>
            {% else %}
                <p>Your cart is empty.</p>
            {% endif %}
            <a href="{{ url_for('index') }}" class="btn btn-primary mt-3">Continue Shopping</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(page, cart_items=cart_items, total=total)


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session.pop('cart', None)  # Clearing cart after checkout
        return redirect(url_for('thank_you'))

    cart_items = [product for product in products if product['id'] in session.get('cart', [])]
    total = sum(item['price'] for item in cart_items)

    page = '''
    <html>
    <head>
        <title>Checkout</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h2>Checkout</h2>
            {% if cart_items %}
                <ul class="list-group">
                {% for item in cart_items %}
                    <li class="list-group-item">
                        {{ item.name }} - ${{ item.price }}
                    </li>
                {% endfor %}
                </ul>
                <p class="mt-3"><strong>Total: ${{ total }}</strong></p>
                <form method="POST">
                    <button type="submit" class="btn btn-success">Confirm and Pay</button>
                </form>
            {% else %}
                <p>Your cart is empty.</p>
            {% endif %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(page, cart_items=cart_items, total=total)


@app.route('/thank_you')
def thank_you():
    page = '''
    <html>
    <head><title>Thank You</title></head>
    <body>
        <div class="container mt-5">
            <h2>Thank you for your order!</h2>
            <a href="{{ url_for('index') }}" class="btn btn-primary">Back to Shopping</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(page)


if __name__ == "__main__":
    app.run(debug=True)


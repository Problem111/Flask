from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import random

app = Flask(__name__)
app.config['GOOGLEMAPS_API_KEY'] = 'AIzaSyB0fP7H2kxhbvroTlVi43VlYLJ90QiLdZo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kokokok'
db = SQLAlchemy(app)
app.jinja_env.globals.update(enumerate=enumerate)


# Function to update data in the CSV file
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    df = pd.read_csv('pizzeria.csv')
    if request.method == 'POST':
        # get data from form
        name = request.form['name']
        price = request.form['price']
        size = request.form['size']
        toppings = request.form['toppings']

        # update the row with the given ID
        df.loc[df['id'] == id, 'Name'] = name
        df.loc[df['id'] == id, 'Price'] = price
        df.loc[df['id'] == id, 'Size'] = size
        df.loc[df['id'] == id, 'Toppings'] = toppings

        # save the updated data to the CSV file
        df.to_csv('pizzeria.csv', index=False)

        # redirect back to the menu page
        return redirect(url_for('menu'))

    else:
        # get the row with the given ID
        row = df.loc[df['id'] == id].iloc[0]
        # render the HTML template with the row data
        return render_template('edit.html', row=row)


# Function to get a random picture from the static folder
@app.route('/picture/<unique_id>')
def picture(unique_id):
    images_dir = 'static/images'
    image_files = os.listdir(images_dir)
    random_image = random.choice(image_files)
    image_path = os.path.join(images_dir, random_image)
    return send_file(image_path, mimetype='image/jpg')

# Database table to store orderhistory


class OrderHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cart_items = db.relationship('Cart', backref='order_history', lazy=True)
    total_price = db.Column(db.Float, nullable=False)

    @staticmethod
    def delete_order_history_for_user(user_id):
        orders = OrderHistory.query.filter_by(user_id=user_id).all()
        for order in orders:
            db.session.delete(order)
        db.session.commit()

# Database table to store users


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

# Database table to store products in shoppingcart


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), autoincrement=True)
    order_history_id = db.Column(db.Integer, db.ForeignKey('order_history.id'))

# Function to add columns to the dataframe


@app.route('/add-data', methods=['GET', 'POST'])
def add_data():
    df = pd.read_csv('pizzeria.csv')
    if request.method == 'POST':
        pizza_id = df['id'].max() + 1
        # get data from form
        new_row = {'id': pizza_id, 'Name': request.form['name'], 'Price': request.form['price'], 'Size': request.form['size'], 'Toppings': request.form['toppings']}
        # append new row to DataFrame
        df = df.append(new_row, ignore_index=True)
        df.to_csv('pizzeria.csv', index=False)
        # redirect back to the homepage or some other page
        return redirect('/menu')
    else:
        # render the HTML template
        return render_template('add_data1.html')

# A new route that contains a function that reads the csv and displays everything in it on the screen


@app.route('/menu')
def menu():
    df = pd.read_csv('pizzeria.csv')
    column_names = list(df.columns.values)  # Convert column names to a list
    row_data = df.values.tolist()
    return render_template("menu.html", column_names=column_names, row_data=row_data)


# Add data route


@app.route("/add_data1")
def add_data1():
    return render_template("add_data1.html")

# Contact route


@app.route("/contact")
def contact():
    return render_template("contact.html")

# Function that makes sure that the first thing that happens is that the database and all tables are created


@app.before_first_request
def create_tables():
    db.create_all()

# Function that creates instances to the table Cart


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    name = request.form['name']
    price = request.form['price']
    user_id = session.get('user_id')
    # Create a new cart item with the selected pizza details
    item = Cart(name=name, price=float(price), quantity=1, user_id=user_id)

    # Add the item to the database session
    flash(f'{item.name} added to cart', 'success')
    db.session.add(item)
    db.session.commit()

    return redirect(url_for('menu'))

# Function that shows everything in the Cart table in the bootstrap.html and calculates the total price


@app.route('/cart')
def view_cart():
    items = Cart.query.all()
    a = 0
    for item in items:
        a += item.price * item.quantity

    return render_template('bootstrap.html', items=items, a=a)

# Function that gets everything in the OrderHistory table that is tied to the current user in the session


@app.route('/order_history')
def order_history():
    user_id = session['user_id']
    order_history_list = OrderHistory.query.filter_by(user_id=user_id).all()
    if order_history_list:
        return render_template('order_history.html', order_history_list=order_history_list)
    else:
        return render_template('order_history.html', message='No order history found.')

# Function that displays everything in the precious function and counts  the total price


@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve the current user's cart items
    user_id = session['user_id']
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return render_template('order_history.html', message='No items found in cart')

    # Calculate the total price of the order
    total_price = sum(item.price * item.quantity for item in cart_items)

    # Create a new OrderHistory object and associate it with the current user
    order_history = OrderHistory(user_id=user_id, total_price=total_price)
    for item in cart_items:
        order_history.cart_items.append(item)

    # Add the new order history object to the database and commit the transaction
    db.session.add(order_history)
    db.session.commit()

    # Clear the user's cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    # Retrieve all the order history for the current user
    order_history_list = OrderHistory.query.filter_by(user_id=user_id).all()

    return redirect(url_for('order_history', order_history_list=order_history_list))

# Function that deletes the selected item from the Cart table


@app.route('/cart/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Cart.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('view_cart'))

# Function that updates the quantity attribute of the selected item in the Cart table


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    item_id = request.json['item_id']
    new_quantity = request.json['new_quantity']

    # Update the quantity of the item in the database
    item = Cart.query.get(item_id)
    item.quantity = new_quantity
    db.session.commit()

    # Return the updated item quantity as JSON data
    return jsonify({'quantity': item.quantity})


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

# Function that register a new user and adds it to the User table


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Function that deletes the selected item from the CSV file which is a column in the dataframe


@app.route('/delete-data/<int:index>', methods=['POST'])
def delete_data(index):
    df = pd.read_csv('pizzeria.csv')
    # delete row at given index
    df.drop(index, inplace=True)
    # save the updated DataFrame
    df.to_csv('pizzeria.csv', index=False)
    # redirect back to the menu page
    return redirect('/menu')

# Function that gets an instance from the User table and checks if the username and password is correct


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:

            session['user_id'] = user.id  # store the user's ID in the session
            session['username'] = username  # store username in session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

# Function that everything in the orderhistory table and pops the user out of the session


@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        OrderHistory.delete_order_history_for_user(user_id)
        session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    

Pizzeria Web App README
Overview

This web application is a simple pizzeria management system that allows users to browse a menu of pizzas, add pizzas to their cart, and manage their orders. The application is built using the Flask web framework and SQLAlchemy for database operations.
Dependencies

    Flask
    Flask-SQLAlchemy
    pandas

Features

    User authentication (login, register, logout)
    Display pizza menu
    Add, edit, and delete pizzas
    Add pizzas to the cart
    Update cart item quantity
    Place an order
    View order history
    Display pizza location with Gooogle Maps API

API Key

The Google Maps API key is stored as a configuration variable, and it should be replaced with your own API key to make use of the Google Maps functionality.
Database

The application uses SQLite for its database and pandas for CSV file operations. The database stores user, cart, and order history data.
Routes

The application contains the following routes:

    /: Index route which directs to the login page
    /login: Login route for user authentication
    /register: Register route for user registration
    /home: Home route for the main page after login
    /logout: Logout route for user logout
    /menu: Displays the pizza menu
    /add-data: Adds a new pizza to the menu
    /edit/<int:id>: Edits the pizza details by ID
    /delete-data/<int:index>: Deletes a pizza from the menu by index
    /picture/<unique_id>: Returns a random pizza image
    /picture1/<unique_id>: Returns a random pizza image (alternative)
    /add_to_cart: Adds a pizza to the user's cart
    /cart: Displays the user's cart
    /cart/delete/<int:id>: Deletes an item from the user's cart by ID
    /update_quantity: Updates the quantity of a cart item
    /place_order: Places an order for the current user
    /order_history: Displays the order history of the current user


Users : 

    username: admin
    password: admin

This username and password combination allows the user to get admin
privelages. Admin privelages allow the user to add, edit, and delete
items from the menu.

Running the Application

To run the application, navigate to the project directory and execute the following command:

bash

python app.py

The application will start in debug mode and can be accessed at http://127.0.0.1:5000/.


from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 

app = Flask(__name__)
mysql = MySQL(app)

# MySQL Database connection function
def get_db_connection():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",        # Your MySQL host (default is localhost)
            user="root",             # MySQL username (replace with your actual MySQL username)
            password="root", # MySQL password (replace with your actual MySQL password)
            database="cloakai_db"       # Database name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to verify the login credentials
def check_credentials(username, password):
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    print(user)
    conn.close()
    
    return user

    # if user:
    #     return True  # User found and credentials match
    # else:
    #     return False  # Invalid username or password


@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (email, password ))
        account = cursor.fetchone()
        if account:
            session['email'] = account['username']
            session['password'] = account['password']
            msg = 'Logged in successfully !'
            
        return msg
    
    # if not data or 'username' not in data or 'password' not in data:
    #     return jsonify({"error": "Username and password are required"}), 400

    # username = data['username']
    # password = data['password']

    # print(username)
    # print(password)
    # # Check the credentials
    # if check_credentials(username, password):
    #     return jsonify({"message": "Login successful!"}), 200
    # else:
    #     return jsonify({"error": "Invalid username or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)  # Disable debug mode



from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='../frontend')

# --- DATABASE CONNECTION HELPER ---
def get_db_connection():
    conn = psycopg2.connect(
        host="ROG",
        database="LungCancer", # Your DB Name
        user="root",           # Your Postgres Username
        password="Root@123"    # Your Postgres Password
    )
    return conn


@app.route('/')
def index():
    
    return render_template('login.html')
# --- SIGN UP ROUTE ---
@app.route('/signup', methods=['POST'])
def signup():
    # 1. Grab data from the HTML form 'name' attributes
    name = request.form['name']
    reason = request.form['reason']
    dob = request.form['dob']
    contact = request.form['contact']
    email = request.form['email']
    password = generate_password_hash(request.form['password']) # Security!

    # 2. Insert into Database
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (full_name, reason, dob, contact, email, password) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, reason, dob, contact, email, password))
        conn.commit()
        return redirect(url_for('login_page')) # Send them to login after success
    except sqlite3.IntegrityError:
        return "Email already registered!"
    finally:
        conn.close()

# --- LOGIN ROUTE ---
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    # 3. Verify Password
    if user and check_password_hash(user['password'], password):
        return redirect(url_for('dashboard')) # Success! Redirect to Lung Cancer Dashboard
    else:
        return "Invalid email or password."

if __name__ == '__main__':
    app.run(debug=True)
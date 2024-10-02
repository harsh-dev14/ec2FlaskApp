from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite setup function
def init_db():
    db_path = '/home/ubuntu/ec2FlaskApp/users.db'  # Use absolute path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT NOT NULL, 
                  password TEXT NOT NULL, 
                  firstname TEXT NOT NULL, 
                  lastname TEXT NOT NULL, 
                  email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('/home/ubuntu/ec2FlaskApp/users.db')
        cursor = conn.cursor()

        # Check for the user in the database
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Welcome {user[2]} {user[3]}, Email: {user[4]}"
        else:
            return "Login failed, please try again."
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Basic validation
        if not all([username, password, first_name, last_name, email]):
            return "All fields are required!", 400

        conn = None  # Initialize conn to None
        try:
            # Save to SQLite3 Database
            conn = sqlite3.connect('/home/ubuntu/ec2FlaskApp/users.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                (username, password, first_name, last_name, email)
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            return f"An error occurred: {str(e)}", 400
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500
        finally:
            if conn:
                conn.close()  # Remove the trailing comma

        return render_template('success.html', first_name=first_name, last_name=last_name, email=email)

    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect('/home/ubuntu/ec2FlaskApp/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)

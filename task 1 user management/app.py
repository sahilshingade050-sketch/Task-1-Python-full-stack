from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# day2 connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#  table
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
        (name, email, age)
    )
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

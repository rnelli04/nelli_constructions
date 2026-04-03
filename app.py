from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY') 

ADMIN_USERNAME = 'nelli'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD') 

def get_db_connection():
    conn = sqlite3.connect('nelli.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return render_template('index.html', projects=projects)

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin.html', projects=projects, messages=messages)

@app.route('/add_project', methods=['POST'])
def add_project():
    title = request.form['title']
    year = request.form['year']
    status = request.form['status']
    area = request.form['area'] # Grab the new area
    description = request.form['description']
    image_file = request.form['image_file']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO projects (title, year, description, status, image_file, area)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, year, description, status, image_file, area))
    
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete_project(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/edit/<int:id>')
def edit_project(id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', project=project)

@app.route('/update/<int:id>', methods=['POST'])
def update_project(id):
    title = request.form['title']
    year = request.form['year']
    status = request.form['status']
    area = request.form['area'] # Grab the updated area
    description = request.form['description']
    image_file = request.form['image_file']

    conn = get_db_connection()
    conn.execute('''
        UPDATE projects
        SET title = ?, year = ?, description = ?, status = ?, image_file = ?, area = ?
        WHERE id = ?
    ''', (title, year, description, status, image_file, area, id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = get_db_connection()
    conn.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', 
                 (name, email, message))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the credentials match
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Give them the VIP wristband!
            return redirect(url_for('admin'))
        else:
            error = "Invalid username or password. Please try again."
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Cut off the VIP wristband
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
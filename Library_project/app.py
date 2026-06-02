from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# CREATE DATABASE
def create_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book TEXT,
            student TEXT,
            status TEXT DEFAULT 'Issued'
        )
    ''')

    conn.commit()
    conn.close()

create_db()


def get_db():
    return sqlite3.connect('library.db')


#HOME 
@app.route('/')
def index():
    return render_template('index.html')


#BOOKS
@app.route('/books')
def books():
    db = get_db()
    data = db.execute("SELECT * FROM books").fetchall()
    db.close()
    return render_template('books.html', books=data)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']

    db = get_db()
    db.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    db.commit()
    db.close()

    return redirect('/books')

@app.route('/delete_book/<int:id>')
def delete_book(id):
    db = get_db()
    db.execute("DELETE FROM books WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect('/books')


#STUDENTS
@app.route('/students')
def students():
    db = get_db()
    data = db.execute("SELECT * FROM students").fetchall()
    db.close()
    return render_template('students.html', students=data)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']

    db = get_db()
    db.execute("INSERT INTO students (name) VALUES (?)", (name,))
    db.commit()
    db.close()

    return redirect('/students')


# ISSUE 
@app.route('/issue')
def issue():
    db = get_db()
    data = db.execute("SELECT * FROM issue").fetchall()
    db.close()
    return render_template('issue.html', data=data)

@app.route('/issue_book', methods=['POST'])
def issue_book():
    book = request.form['book']
    student = request.form['student']

    db = get_db()
    db.execute("INSERT INTO issue (book, student) VALUES (?, ?)", (book, student))
    db.commit()
    db.close()

    return redirect('/issue')

@app.route('/return_book/<int:id>')
def return_book(id):
    db = get_db()
    db.execute("UPDATE issue SET status='Returned' WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect('/issue')


if __name__ == '__main__':
    app.run(debug=True)
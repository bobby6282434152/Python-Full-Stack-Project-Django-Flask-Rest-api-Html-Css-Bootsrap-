from flask import Flask, redirect, render_template, request, url_for 
from models import db, Student
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# @app.route('/')
# def home():
#     return redirect(url_for())

#Add Students
@app.route('/add_data', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        student = Student(name=name, age=age, course=course)
        db.session.add(student)
        db.session.commit()
        return redirect('dashboard')
    return render_template('add_student.html')

#view students
@app.route('/dashboard')
def get_all_students():
    students = Student.query.all()
    return render_template('view_student.html', students=students)

#update students
@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.course = request.form['course']

        db.session.commit()
        return redirect('/dashboard')
    return render_template('update_student.html', student=student)

#delete students
@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)
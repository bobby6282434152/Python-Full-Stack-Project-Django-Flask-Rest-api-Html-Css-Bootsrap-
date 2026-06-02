from flask import Flask,request,jsonify
from models import db,Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# above are configutions 


# home page url and views starts here
@app.route('/')
def home():
    return jsonify({
        'message':'flask restapi is working'
    })

# Get all students url and views starts here
@app.route('/get_students',methods=['GET'])
def get_students():

    students = Student.query.all()

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list)
  
# Get a sinngle student url and views starts here
@app.route('/single_student/<int:id>/', methods=['GET'])
def get_single_student(id):

    single_student = Student.query.get(id)
   
    if not single_student:
        return jsonify({
            'message':'student not found'
        }), 404
    return jsonify(single_student.to_dict())


# post student url and views starts here
@app.route('/add_students' , methods=['POST'])
def add_students():

    # recive json data
    data = request.get_json()

    # create object
    new_student = Student(
        name=data['name'],
        course=data['course']
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        'message':'student data added successfully',
        'student':new_student.to_dict()
    }),201

@app.route('/delete_students/<int:id>/',methods=['DELETE'])
def delete_student(id):
    get_student = Student.query.get(id)
    if not get_student:
        return jsonify({
            'message': 'Student not found'
        }), 404
        
    db.session.delete(get_student)
    db.session.commit()

    return jsonify({
        'message': 'Student deleted successfully'
    }), 200

@app.route('/update_data/<int:id>',methods=['PUT'])
def alter_data(id):
    student = Student.query.get(id)

    data = request.get_json()
    
    student.name = data['name']
    student.course = data['course']
    db.session.commit()

    return jsonify({
        'message':'data succesfully updated'
    })

# below are configutions 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)  


from flask import Flask, request, flash, url_for, redirect, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random_string"

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/')
def hello_world():
    return {"Hello": "World!"}

@app.route('/get')
def show_all():
    return render_template('index.html', students=Student.query.all())

@app.route('/new', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data.get('name') or not data.get('city') or not data.get('addr'):
        return {"message": "Please enter all the fields"}, 400
    else:
        student = Student(data['name'], data['city'], data['addr'], data.get('pin', ''))
        db.session.add(student)
        db.session.commit()
        return {"message": "Record was successfully added"}, 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        new_student = Student(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            dob=dob,
            amount_due=request.form['amount_due']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('get_students'))
    return render_template('add_student.html')

@app.route('/student/<int:id>', methods=['GET'])
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('student.html', student=student)

@app.route('/student/<int:id>/edit', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.dob = dob
        student.amount_due = request.form['amount_due']
        db.session.commit()
        return redirect(url_for('get_students'))
    return render_template('edit_student.html', student=student)

@app.route('/student/<int:id>', methods=['POST'])
def update_delete_student(id):
    student = Student.query.get_or_404(id)
    if request.form['_method'] == 'DELETE':
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('get_students'))
    return redirect(url_for('edit_student', id=id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

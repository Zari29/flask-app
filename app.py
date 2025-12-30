from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    student = Student(
        fname=request.form['fname'],
        lname=request.form['lname'],
        email=request.form['email']
    )
    db.session.add(student)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:sno>")
def delete(sno):
    student = Student.query.filter_by(sno=sno).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    student = Student.query.filter_by(sno=sno).first()
    if request.method == "POST":
        student.fname = request.form['fname']
        student.lname = request.form['lname']
        student.email = request.form['email']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", student=student)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=False)

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect  # ✅ Add this


import re

app = Flask(__name__)

# ---------------------------------
# 1️⃣ Secure Configurations
# ---------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'i2216572025z2A3r4L!5h0098@7766#Zr$LiSH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secureapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False   # Must be False for localhost
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf = CSRFProtect(app)  # initialize AFTER setting secret key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ---------------------------------
# 2️⃣ Define database model
# ---------------------------------
class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"

# ---------------------------------
# 3️⃣ Secure Input Handling using Flask-WTF Validators
# ---------------------------------
class StudentForm(FlaskForm):
    fname = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
        Regexp(r'^[A-Za-z]+$', message="First name must contain only letters")
    ])
    lname = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
        Regexp(r'^[A-Za-z]+$', message="Last name must contain only letters")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address")
    ])
    submit = SubmitField('Submit')

# ---------------------------------
# 4️⃣ Routes
# ---------------------------------
@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)

# CREATE — uses form validation
@app.route("/add", methods=["GET", "POST"])
def add():
    form = StudentForm()
    if form.validate_on_submit():
        # Sanitize: Prevent SQL keywords or HTML injection manually
        def safe_input(value):
            return re.sub(r'[<>{};]', '', value)  # strip HTML special chars

        fname = safe_input(form.fname.data)
        lname = safe_input(form.lname.data)
        email = safe_input(form.email.data)

        # Parameterized ORM insert (SQLAlchemy handles this safely)
        student = Student(fname=fname, lname=lname, email=email)
        db.session.add(student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect("/")
    return render_template("add.html", form=form)

# DELETE — parameterized via ORM
@app.route("/delete/<int:sno>")
def delete(sno):
    student = Student.query.get_or_404(sno)
    db.session.delete(student)
    db.session.commit()
    flash("Record deleted successfully!", "info")
    return redirect("/")

# UPDATE — safe validation and CSRF
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    student = Student.query.get_or_404(sno)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.fname = re.sub(r'[<>{};]', '', form.fname.data)
        student.lname = re.sub(r'[<>{};]', '', form.lname.data)
        student.email = re.sub(r'[<>{};]', '', form.email.data)
        db.session.commit()
        flash("Student record updated successfully!", "success")
        return redirect("/")
    return render_template("update.html", form=form, student=student)

# ---------------------------------
# 5️⃣ Custom Error Pages
# ---------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ---------------------------------
# 6️⃣ Example Secure Password Hashing (for future use)
# ---------------------------------
@app.route("/hash/<password>")
def hash_password(password):
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    return f"Hashed Password: {hashed}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
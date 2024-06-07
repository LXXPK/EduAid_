from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,text
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://root:@localhost/test')  # Adjust as needed
db = SQLAlchemy(app)


# Initialize Flask-Login for user authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set the login view route

# Define a user loader function to retrieve users by ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the User class to represent users in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)

# Define the Students class to represent student information in the database
class Students(UserMixin, db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_usn = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(1000), unique=True, nullable=False)
    phone_number = db.Column(db.String(1000), nullable=False)
    gender = db.Column(db.String(1000), nullable=False)
    section = db.Column(db.String(1000), nullable=False)
    year_of_studying = db.Column(db.String(1000), nullable=False)
    semester = db.Column(db.String(1000), nullable=False)
    year_of_joining = db.Column(db.String(1000), nullable=False)
    department = db.Column(db.String(1000), nullable=False)
    course = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    address2 = db.Column(db.String(1000), nullable=False)
    city = db.Column(db.String(1000), nullable=False)
    state = db.Column(db.String(1000), nullable=False)
    zipcode = db.Column(db.String(1000), nullable=False)

# Define the route for the home page
@app.route("/")
def home():
    if 'username' in session:
        return render_template('home.html', username=current_user.usernames)
    else:
        return render_template('index.html')

# Define the route for user login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', "danger")
            return render_template('login.html')
    else:
        return render_template('login.html')

# Define the route for user signup
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists", "danger")
            return render_template('signup.html')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')

# Define the route for user logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Define the route for the question paper page
@app.route("/q_paper")
@login_required
def q_paper():
    return render_template('q_paper.html')

# Define the route for the schedule page
@app.route("/schedule")
@login_required
def schedule():
    return render_template('schedule.html', username=current_user.username)

# Define the route for the student information page
@app.route("/student_info")
@login_required
def student_info():
    return render_template('student_info.html')

# Define the route and functionality for updating student information
@app.route("/student_update", methods=['GET', 'POST'])
@login_required
def student_update():
    if request.method == 'POST':
        # Extract form data
        student_usn = request.form['student_usn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        email=request.form['email']
        phone_number=request.form['phone_number']
        gender=request.form['gender']
        section=request.form['section']
        year_of_studying=request.form['year_of_studying']
        semester=request.form['semester']
        year_of_joining=request.form['year_of_joining']
        department=request.form['department']
        course=request.form['course']
        address=request.form['address']
        address2=request.form['address2']
        city=request.form['city']
        state=request.form['state']
        zipcode=request.form['zipcode']

        # Construct raw SQL query
        sql_query = """
            INSERT INTO Students (
                student_usn, first_name, last_name, date_of_birth, email, phone_number, 
                gender, section, year_of_studying, semester, year_of_joining, 
                department, course, address, address2, city, state, zipcode
            ) VALUES (
                :student_usn, :first_name, :last_name, :date_of_birth, :email, :phone_number, 
                :gender, :section, :year_of_studying, :semester, :year_of_joining, 
                :department, :course, :address, :address2, :city, :state, :zipcode
            )
        """

        try:
            with db.engine.connect() as connection:
                connection.execute(text(sql_query), {
                    'student_usn': student_usn,
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': date_of_birth,
                    'email': email,
                    'phone_number': phone_number,
                    'gender': gender,
                    'section': section,
                    'year_of_studying': year_of_studying,
                    'semester': semester,
                    'year_of_joining': year_of_joining,
                    'department': department,
                    'course': course,
                    'address': address,
                    'address2': address2,
                    'city': city,
                    'state': state,
                    'zipcode': zipcode
                })
                db.session.commit()
                flash('Student information updated successfully', 'success')
        except Exception as e:
            flash(f'Error adding student information: {str(e)}', 'danger')

    return render_template('student_update.html')

# Define the route for the internal assessment average page
@app.route("/ia_avg")
@login_required
def ia_avg():
    return render_template('IA_avg.html')

# Define the route for editing student information
@app.route("/edit")
@login_required
def edit_stu():
    return render_template('edit_student_update.html')

# Define the route for the seating matrix page
@app.route("/seating_matrix")
@login_required
def seating_matrix():
    return render_template('seating_matrix.html')

# Define the route for the user profile page
@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

# Run the Flask app if this file is executed
if __name__ == "__main__":
    app.run(debug=True)

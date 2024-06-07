from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required
from flask_login import LoginManager

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_strong_secret_key'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hms'  # Adjust as needed
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)

@app.route("/")
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('index.html')

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
            return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error='Email already exists')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/q_paper")
@login_required
def q_paper():
    return render_template('q_paper.html')
@app.route("/schedule")
@login_required
def schedule():
    return render_template('schedule.html')
@app.route("/student_info")
@login_required
def student_info():
    return render_template('student_info.html')
@app.route("/seating_matrix")
@login_required
def seating_matrix():
    return render_template('seating_matrix.html')

if __name__ == "__main__":
    app.run(debug=True)

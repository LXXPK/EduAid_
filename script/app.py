from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,logout_user,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
#  my database connection
local_server=True
app = Flask(__name__)
app.secret_key='kumar'


# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databse_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hms'
db=SQLAlchemy(app)


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User( UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    email=db.Column(db.String(100),unique=True)
    password=db.column(db.String(1000))

@app.route("/")
def home():
    return render_template('index.html')
    
@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/logout")
def logout():
    return render_template('login.html')
@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            print("email already exists ")
            return render_template('signup.html')
        
        # new_user=db.engine.execute(f"INSERT INTO 'user' ('username','email','password') VALUES('KIRAN','REDDY@GMAIL.COM','RAMANA') ")  
        encpassword=generate_password_hash(password)  
        new_user = db.session.execute(
    text(f"INSERT INTO `user` (`username`, `email`, `password`) VALUES (:username, :email, :encpassword)"),
    {'username': username, 'email': email, 'encpassword': encpassword})

    
        return render_template('login.html')
        # print(username,email,password)

    #     print("this is get methos ")
    # print("this is get method")
    return render_template('signup.html')
@app.route("/q_paper")
def q_paper():
    return render_template('q_paper.html')
@app.route("/schedule")
def schedule():
    return render_template('schedule.html')
@app.route("/student_info")
def student_info():
    return render_template('student_info.html')
@app.route("/seating_matrix")
def seating_matrix():
    return render_template('seating_matrix.html')

# @app.route("/home")
# def home():
#     try:
#         Test.query.all()
#         return 'my databse is connected'
#     except:
#         return 'not connected'

if __name__ == "__main__":
    print("hhi")
    app.run(debug=True)
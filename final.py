from flask import Flask, render_template, request, session, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_user, logout_user,login_required,current_user
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'eduaid321'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hms'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)

class Students(UserMixin, db.Model):
    student_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    student_usn = db.Column(db.String(50),unique=True, nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(1000),unique=True, nullable=False)
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


class Questions(UserMixin, db.Model):
    paper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20),unique=True, nullable=False)

    date = db.Column(db.String(20) , nullable=False)
    sub_name = db.Column(db.String(40) , nullable=False)
    sub_code = db.Column(db.String(40) , nullable=False)
    question1 = db.Column(db.String(1000) , nullable=False)
    question2 = db.Column(db.String(1000), nullable=False)
    question3 = db.Column(db.String(1000), nullable=False)
    question4 = db.Column(db.String(1000), nullable=False)
    question5 = db.Column(db.String(1000), nullable=False)
    question6 = db.Column(db.String(1000), nullable=False)
    question7 = db.Column(db.String(1000), nullable=False)
    question8 = db.Column(db.String(1000), nullable=False)
    question9 = db.Column(db.String(1000), nullable=False)
    question10 = db.Column(db.String(1000), nullable=False)

class Room(UserMixin,db.Model):
    room_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_no=db.Column(db.String(10), nullable=False)
    col=db.Column(db.String(10)  , nullable=False)
    row=db.Column(db.String(10) , nullable=False)
    seat=db.Column(db.String(10) , nullable=False)


class Timetable(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    subject_names = db.Column(db.Text)
    teachers_list = db.Column(db.Text)
    slots_per_week = db.Column(db.Text)
    days_in_week = db.Column(db.Integer)
    slots_per_day = db.Column(db.Integer)
    time_per_slot = db.Column(db.String(10))
    start_time=db.Column(db.String(10))
    repetation=db.Column(db.String(10))



      
        
@app.route("/")
def home():
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
            flash( 'Invalid email or password',"danger")
            return render_template('login.html')
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
            flash("Email already exists","danger")
            return render_template('signup.html')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


days = ['',"Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"]




@app.route("/saved_schedules", methods=['POST','GET'])
@login_required
def saved_schedule():
    query=Timetable.query.all()
    return render_template('saved_schedules.html',query=query)



@app.route("/schedule", methods=['POST','GET'])
@login_required
def schedule():
    if request.method == 'POST':
        id=request.form['id']
        days_in_week = request.form.get('days_in_week')
        slots_per_day = request.form.get('slots_per_day')
        subject_names = request.form.getlist('subjectName[]')
        teachers_list = request.form.getlist('teachers[]')
        slots_per_week_list = request.form.getlist('slotsPerWeek[]')
        time_per_slot = request.form.get('time_per_slot')
        start_time = request.form.get('start_time')
        repetation = request.form.get('repetation')

        

        exists=Timetable.query.filter_by(id=id).first()
        if exists:
            flash("the Schedule already exists give other ID","danger")
            return render_template('schedule.html')
        
        else:

        
            subject_names_str = ','.join(subject_names)
            teachers_list_str = ','.join(teachers_list)
            slots_per_week_str = ','.join(slots_per_week_list)

        
            timetable = Timetable(
                id=id,
            subject_names=subject_names_str,
            teachers_list=teachers_list_str,
            slots_per_week=slots_per_week_str,
            days_in_week=days_in_week,
            slots_per_day=slots_per_day
            ,start_time=start_time,
            time_per_slot=time_per_slot
            ,repetation=repetation
                )
            db.session.add(timetable)
            db.session.commit()
            flash("Schedule saved successfully","success")
            return render_template('schedule.html')


    else:
        return render_template('schedule.html')


@app.route("/delete_timetable/<int:id>", methods=['POST', 'GET'])
def delete_timetable(id):
    try:
        
        timetable_to_delete = Timetable.query.get(id)

        if timetable_to_delete:
            
            db.session.delete(timetable_to_delete)

            
            db.session.commit()

            flash('Saved  data deleted successfully!', 'success')
            return render_template('saved_schedules.html')
        else:
            flash('Student not found!', 'danger')
            return render_template('saved_schedules.html')

    except Exception as e:
        
        flash(f'Error deleting data: {str(e)}', 'danger')

    return render_template('saved_schedules.html')
    


@app.route('/preview_timetable/<int:id>')
@login_required
def preview_timetable(id):
    query=Timetable.query.all()
    
    timetable_data=Timetable.query.filter_by(id=id).first()
    sub=timetable_data.subject_names.split(',')
    print("timetable_data:", timetable_data)
    print("sub:", sub)
    if(timetable_data.slots_per_day>len(sub)):
        print("1stif")
        if timetable_data.repetation=="allow":
            print("2ndif")
            generated_timetable=repetation(timetable_data)
            print("Generated timetable (with repetation):", generated_timetable)
            time_slots=generate_time_slots(timetable_data.start_time, timetable_data.time_per_slot,timetable_data.slots_per_day)
            start_time=timetable_data.start_time
            time_per_slot=timetable_data.time_per_slot
            print("Generated time slots:", time_slots)
            print("Start time:", start_time)
            print("Time per slot:", time_per_slot)
            return render_template('preview_timetable.html',data=generated_timetable,start_time=start_time,time_per_slot=time_per_slot,time_slots=time_slots,days=days)
        else:
            print("3rdif")
            flash("Without repetation creation of time table is not possible ","danger")
            return render_template('saved_schedules.html',query=query)
    else:
        print("4thif")
        generated_timetable=generate_timetable(timetable_data)
        print("Generated timetable:", generated_timetable)
        time_slots=generate_time_slots(timetable_data.start_time, timetable_data.time_per_slot,timetable_data.slots_per_day)
        start_time=timetable_data.start_time
        time_per_slot=timetable_data.time_per_slot
        print("Generated time slots:", time_slots)
        print("Start time:", start_time)
        print("Time per slot:", time_per_slot)
        return render_template('preview_timetable.html',data=generated_timetable,start_time=start_time,time_per_slot=time_per_slot,time_slots=time_slots,days=days)

    


    

def generate_time_slots(start_time, time_per_slot, num_slots_per_day):
    print("slots is working 1")
    # Convert time_per_slot to an integer
    time_per_slot = int(time_per_slot)


    # Parse start_time
    try:
        start_datetime = datetime.strptime(start_time, '%H:%M')
    except ValueError:
        # Handle the case where start_time is in an invalid format
        return []

    # Calculate end_datetime for each slot and format the time slots
    time_slots = []
    for _ in range(num_slots_per_day):
        end_datetime = start_datetime + timedelta(minutes=time_per_slot)
        time_slot_str = f"{start_datetime.strftime('%I:%M %p')} to {end_datetime.strftime('%I:%M %p')}"
        time_slots.append(time_slot_str)
        start_datetime = end_datetime
    print("slots is working 2")
    return time_slots



def generate_timetable(timetable_data):
    days = timetable_data.days_in_week
    slots_per_day = timetable_data.slots_per_day
    subjects = timetable_data.subject_names.split(',')
    teachers = timetable_data.teachers_list.split(',')

    if len(subjects) > len(teachers):
        raise ValueError("Insufficient number of teachers for the subjects")

    timetable = {}
    for day in range(1, days + 1):
        timetable[day] = {}
        for slot in range(1, slots_per_day + 1):
            timetable[day][slot] = {'subject': None, 'teacher': None}

    subject_teacher_mapping = dict(zip(subjects, teachers))

    # Track the subjects already assigned to each day
    assigned_subjects_per_day = {day: set() for day in range(1, days + 1)}

    for day in range(1, days + 1):
        for slot in range(1, slots_per_day + 1):
            shuffled_subjects = subjects.copy()
            random.shuffle(shuffled_subjects)
            for subject in shuffled_subjects:
                # Check if the subject has already been assigned to the current day
                if subject not in assigned_subjects_per_day[day]:
                    teacher = subject_teacher_mapping[subject]
                    timetable[day][slot]['subject'] = subject
                    timetable[day][slot]['teacher'] = teacher
                    assigned_subjects_per_day[day].add(subject)
                    break  # Move to the next slot

    return timetable





def repetation(timetable_data):
    days = timetable_data.days_in_week
    slots_per_day = timetable_data.slots_per_day
    subjects = timetable_data.subject_names.split(',')
    teachers = timetable_data.teachers_list.split(',')

    # Ensure that there are enough teachers for the subjects
    if len(subjects) > len(teachers):
        raise ValueError("Insufficient number of teachers for the subjects")

    # Initialize the timetable
    timetable = {}
    for day in range(1, days + 1):
        timetable[day] = {}
        for slot in range(1, slots_per_day + 1):
            timetable[day][slot] = {'subject': None, 'teacher': None}

    # Assign subjects to slots
    subject_teacher_mapping = dict(zip(subjects, teachers))
    slots_per_week_list = timetable_data.slots_per_week.split(',')
    if len(slots_per_week_list) != len(subjects):
        raise ValueError("Mismatch in the number of subjects and slots per week")

    for subject, slots_per_week in zip(subjects, slots_per_week_list):
        teacher = subject_teacher_mapping[subject]
        slots_remaining = int(slots_per_week)

        # Assign the subject to slots based on the specified number of slots per week
        while slots_remaining > 0:
            day = random.randint(1, days)
            slot = random.randint(1, slots_per_day)

            if timetable[day][slot]['subject'] is None:
                timetable[day][slot]['subject'] = subject
                timetable[day][slot]['teacher'] = teacher
                slots_remaining -= 1

    return timetable



@app.route("/student_info")
@login_required
def student_info():
    query=Students.query.all() 
    return render_template('student_info.html',query=query)
    
@app.route("/student_update",methods=['GET', 'POST'])
@login_required
def student_update():
    if request.method == 'POST':
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

        
        
        existing_student = Students.query.filter_by(student_usn=student_usn,email=email).first()
        if existing_student:
            flash("Student already exist","danger")
            return render_template('student_update.html')
        else:
            new_student = Students(student_usn=student_usn,	first_name=first_name,	last_name=last_name,	date_of_birth=date_of_birth,	email=email,	phone_number=phone_number,	gender=gender,	section=section,	year_of_studying=year_of_studying,	semester=semester,	year_of_joining=year_of_joining,	department=department,	course=course,	address=address,	address2=address2,	city=city,	state=state,	zipcode=zipcode	)
            db.session.add(new_student)
            db.session.commit()
            flash('Student information updated successfully', 'success')
            return render_template('student_update.html')  
    else:
      
        return render_template('student_update.html')





    
@app.route("/edit/<string:student_id>",methods=['POST','GET'])
@login_required
def edit_stu(student_id):
    posts=Students.query.filter_by(student_id=student_id).first()
    if request.method == 'POST':
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
        try:
        
            student=Students.query.filter_by(student_id=student_id).first()

        
            student.student_usn = student_usn
            student.first_name = first_name
            student.last_name = last_name
            student.date_of_birth = date_of_birth
            student.email = email
            student.phone_number = phone_number
            student.gender = gender
            student.section = section
            student.year_of_studying = year_of_studying
            student.semester = semester
            student.year_of_joining = year_of_joining
            student.department = department
            student.course = course
            student.address = address
            student.address2 = address2
            student.city = city
            student.state = state
            student.zipcode = zipcode

        # Commit the changes to the database
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('student_info'))
        except Exception as e:
            flash(f'Error updating student: {e}', 'danger')
            return render_template('student_edit.html')
       
    return render_template('student_edit.html',posts=posts)



@app.route("/view/<string:student_id>")
@login_required
def view_stu(student_id):
  
  student=Students.query.filter_by(student_id=student_id).first()
  return render_template('student_view.html',posts=student)



@app.route("/delete/<int:student_id>", methods=['POST', 'GET'])
def delete_student(student_id):
    try:
        
        student_to_delete = Students.query.get(student_id)

        if student_to_delete:
            
            db.session.delete(student_to_delete)

            
            db.session.commit()

            flash('Student deleted successfully!', 'success')
            return redirect(url_for('student_info'))
        else:
            flash('Student not found!', 'danger')
            return redirect(url_for('student_info'))

    except Exception as e:
        
        flash(f'Error deleting student: {str(e)}', 'danger')

    return redirect(url_for('student_info'))



@app.route("/q_paper",methods=['GET','POST'])
@login_required
def q_paper():
    if request.method=='POST':
        code=request.form['code']

        date=request.form['date']    
        sub_name=request.form['sub_name']    
        sub_code=request.form['sub_code']    
        question1=request.form['question1']    
        question2=request.form['question2']    
        question3=request.form['question3']
        question4=request.form['question4']
        question5=request.form['question5']
        question6=request.form['question6']
        question7=request.form['question7']
        question8=request.form['question8']
        question9=request.form['question9']
        question10=request.form['question10']
        existing_code = Questions.query.filter_by(code=code).first() 
        if existing_code:
           
            flash("Code already exist","danger")
            return redirect(url_for('q_paper'))
        else:
            questions = Questions(code=code,date=date,sub_name=sub_name,sub_code=sub_code,question1=question1,question2=question2,question3=question3,question4=question4,question5=question5,question6=question6,question7=question7,question8=question8,question9=question9,question10=question10)
            db.session.add(questions)
            db.session.commit()
            flash('Data saved successfully', 'success')
            return redirect(url_for('q_paper'))
    else:
      
        return render_template('q_paper.html')
         
@app.route('/saved_qp')
@login_required
def saved_qp():
    query=Questions.query.all() 
    return render_template('saved_qp.html',query=query)

@app.route("/paper_copy/<string:code>")
@login_required
def paper_copy(code):
    paper=Questions.query.filter_by(code=code).first()
    return render_template("paper_copy.html",posts=paper)


@app.route("/seating_matrix")
@login_required
def seating_matrix():
    query=Room.query.all()
    return render_template('seating_matrix.html',query=query)
    
       
@app.route("/add_room",methods=['GET', 'POST'])
@login_required
def add_room():
    if request.method == 'POST':
        room_no=request.form['room_no']
        col=request.form['col']
        row=request.form['row']
        seat=request.form['seat']
        existing_room = Room.query.filter_by(room_no=room_no).first() 
        if existing_room:
            flash("Room already exist","danger")
            return redirect(url_for('add_room'))
        else:
            new_room=Room(room_no=room_no,row=row,col=col,seat=seat)
            db.session.add(new_room)
            db.session.commit()
            flash('Data saved successfully', 'success')
            return redirect(url_for('add_room'))
    else:
      
        return render_template('add_room.html')
    

@app.route("/delete_room/<int:room_no>", methods=['POST', 'GET'])
def delete_room(room_no):
    try:
        
        room_to_delete = Room.query.get(room_no)

        if room_to_delete:
            
            db.session.delete(room_to_delete)

            
            db.session.commit()

            flash('Room deleted successfully!', 'success')
            return redirect(url_for('seating_matrix'))
        else:
            flash('Room not found!', 'danger')
            return redirect(url_for('seating_matrix'))

    except Exception as e:
        
        flash(f'Error deleting room: {str(e)}', 'danger')

    return redirect(url_for('seating_matrix'))

@app.route("/generate", methods=['POST', 'GET'])
@login_required
def generate():
    if request.method == 'POST':
        room_no = request.form['room_no']
        missing_l = request.form['missing'].split(',')
        print(missing_l)
        query = Room.query.filter_by(room_no=room_no).first()
        row = int(query.row)
        col = int(query.col)
        seat = int(query.seat)
        
        # Initialize lists to store student groups
        student_groups = []

        
        for key, value in request.form.items():
            if key.startswith('start'):
                
                start_str = value
                end_str = request.form['end' + key[5:]]

                
                start_num = int(start_str[-3:])
                end_num = int(end_str[-3:])

                
                student_group = [start_str[:7] + str(num).zfill(3) for num in range(start_num, end_num + 1)]
                student_groups.append(student_group)

        
        student_groups_without_missing = []
        for group in student_groups:
            for student in group:
                if student in missing_l:
                    group.remove(student)
            student_groups_without_missing.append(group)

        
        print("Student Groups:", student_groups)
        print("Student Groups without Missing Values:", student_groups_without_missing)
        
        
        total_students = sum(len(group) for group in student_groups_without_missing)
        if total_students > int(seat):
            flash('Students exceed the limit of seats in the class.', 'error')
            return render_template('generate.html')

        
        seating_arr = generate_seating_arrangement(student_groups_without_missing,  col,row)
        print(seating_arr)
        session['seating_arr'] = seating_arr
        print("Seating Arrangement:")
        
        return redirect(url_for('seating_view', seating_arr=seating_arr))
    else:
        return render_template('generate.html')

    
def generate_seating_arrangement(student_groups, row, col):
    temp_matrix = [[''] * col for _ in range(row)]
    group_index = 0

    for i in range(row):
        for j in range(col):
            # Check if all student groups have been processed
            if group_index >= len(student_groups):
                group_index = 0
            
            # If there are still students in the current group, assign them to seats
            if student_groups[group_index]:
                # Fill the seat if it's available
                if temp_matrix[i][j] == '':
                    temp_matrix[i][j] = student_groups[group_index].pop(0)
            
            # Move to the next group for the next seat
            group_index += 1

    # Check if there are still students left in any group
    for group in student_groups:
        if group:
            # If there are still students left, fill remaining empty seats with them
            for i in range(row):
                for j in range(col):
                    if group and temp_matrix[i][j] == '':
                        temp_matrix[i][j] = group.pop(0)

    # Return the seating arrangement
    return temp_matrix


@app.route('/seating_view',methods=['POST','GET'])
@login_required
def seating_view():
    seating_arr = session.get('seating_arr')
    return render_template('seating_view.html',seating_arr=seating_arr)





@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html',username=current_user.username,email=current_user.email)



if __name__ == "__main__":
    app.run(debug=True)

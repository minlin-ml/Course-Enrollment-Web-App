
from application import app, db
from flask import Response, redirect, render_template, request, json, flash, redirect, url_for, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
  return render_template("index.html", index=True)

@app.route("/login", methods=["GET", "POST"])
def login():
  if session.get('username'):
    return redirect(url_for('index'))

  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = User.objects(email=email).first()
    if user and user.get_password(password):
      flash("You are successfully logged in!", "success")
      session['user_id'] = user.user_id
      session['username'] = user.first_name
      return redirect("/index")
    else:
      flash("Something might went wrong, please try again!", "danger")
  return render_template("login.html", title= 'Login', form=form, login=True)

@app.route("/courses")
@app.route("/courses/<term>") 
def courses(term=None):
  if term is None:
    term = "Spring 2019"

  classes = Course.objects.order_by('courseID')
  return render_template("courses.html", courseData=classes, courses=True, term=term)

@app.route("/register", methods=["GET", "POST"])
def register():
  if session.get('username'):
    return redirect(url_for('index'))
  form = RegisterForm()
  if form.validate_on_submit():
    user_id = User.objects.count()
    user_id += 1

    email = form.email.data
    password = form.password.data
    first_name = form.first_name.data
    last_name = form.last_name.data

    user = User(user_id = user_id,
                first_name = first_name,
                last_name = last_name,
                email = email
                )
    user.set_password(password)
    user.save()
    flash("You're successfully registered!", "success")
    return redirect(url_for('index'))
    
  return render_template("register.html", title='Register', form=form, register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
  courseID = request.form.get('courseID')
  courseTitle = request.form.get('title')
  user_id = 1
  if courseID:
    if Enrollment.objects(user_id=user_id, courseID=courseID):
      flash(f"Opps! You are already registered in this course {courseTitle}!","danger" )
      return redirect(url_for('courses'))
    else:
      Enrollment(user_id=user_id,courseID=courseID).save()
      flash(f"You registered to {courseTitle} successfully!", "success")
  classes = list(User.objects.aggregate(*[
          {
              '$lookup': {
                  'from': 'enrollment', 
                  'localField': 'user_id', 
                  'foreignField': 'user_id', 
                  'as': 'r1'
              }
          }, {
              '$unwind': {
                  'path': '$r1', 
                  'includeArrayIndex': 'r1.id', 
                  'preserveNullAndEmptyArrays': False
              }
          }, {
              '$lookup': {
                  'from': 'course', 
                  'localField': 'r1.courseID', 
                  'foreignField': 'courseID', 
                  'as': 'r2'
              }
          }, {
              '$unwind': {
                  'path': '$r2', 
                  'preserveNullAndEmptyArrays': False
              }
          }, {
              '$match': {
                  'user_id': user_id
              }
          }, {
              '$sort': {
                  'courseID': 1
              }
          }
      ]))
  term = request.form.get('term')
  return render_template("enrollment.html", enrollment=True, title = "Enrollment", classes=classes)

@app.route("/api/") 
@app.route("/api/<idx>")
def api(idx=None):
  if(idx==None):
    jsonData = courseData
  else:
    jsonData = courseData[int(idx)]
  return Response(json.dumps(jsonData), mimetype="application/json")


  
@app.route("/user")
def user():
  # User(user_id = '1', first_name = 'Min', last_name = 'Lin', email = 'min-lin@hotmail.com', password = 'test123').save()
  # User(user_id = '2', first_name = 'Tom', last_name = 'Hank', email = 'th@hotmail.com', password = 'thtest123').save()
  users = User.objects.all()
  return render_template("user.html", users = users)


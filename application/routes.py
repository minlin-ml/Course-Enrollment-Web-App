
from application import app, db
from flask import Response, redirect, render_template, request, json, flash, redirect
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
  return render_template("index.html", index=True)

@app.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if request.form.get("email") == "test@utm.org":
      flash("You are successfully logged in!", "success")
      return redirect("/index")
    else:
      flash("Something might went wrong, please try again!", "danger")
  return render_template("login.html", title= 'Login', form=form, login=True)

@app.route("/courses")
@app.route("/courses/<term>") 
def courses(term="2019"):
  

  return render_template("courses.html", courseData=courseData, courses=True, term=term)

@app.route("/register")
def register():
  return render_template("register.html", register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
  id = request.form.get('courseID')
  title = request.form.get('title')
  term = request.form.get('term')
  return render_template("enrollment.html", enrollment=True, data={"id": id, "title": title, "term": term})

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


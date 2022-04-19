from unittest.util import _MAX_LENGTH
import flask
from application import db

class User(db.Document):
  user_id = db.IntField(unique=True)
  first_name = db.StringField(maxLength=50)
  last_name = db.StringField(maxLength=50)
  email = db.StringField(maxLength=50)
  password = db.StringField(maxLength=50)

class Course(db.Document):
  course_id = db.StringField( max_length=10, unique=True)
  title = db.StringField( max_length=100)
  description = db.StringField( max_length=255)
  credicts = db.IntField()
  term = db.StringField( max_length=25)

class Enrollment(db.Document):
  user_id = db.IntField()
  course_id = db.StringField( max_length=10)


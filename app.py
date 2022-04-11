from flask import Flask, redirect, render_template,session, url_for, request
from functools import wraps
import pymongo
import gridfs
import os
from werkzeug.utils import secure_filename
from filter import *
from flask_sqlalchemy import SQLAlchemy 



app=Flask(__name__)
app.secret_key='intelligentetlprojecthoussemamanisupervisedbymaherheni'


client=pymongo.MongoClient("mongodb+srv://houssem:05347268hO.@cluster0.e0gv8.mongodb.net/test")
db=client.etl
files=gridfs.GridFS(db)


# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

 #routes
from user.routes import *
from user.upload import My_SQL_Form, UploadFileForm

@app.route('/')
def home():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('signup.html')
import mysql.connector
from mysql.connector import Error
@app.route('/extract',methods=['GET','POST'])
@login_required
def extract():
    mysql_form=My_SQL_Form()
    if mysql_form.validate_on_submit():
        user = request.form.get('user') 
        password=request.form.get('password')
        host=request.form.get('host')
        database=request.form.get('database')
        
        
        connection = mysql.connector.connect(host=request.form.get('host'),
                                     database=request.form.get('database'),
                                         user = request.form.get('user'),
                                         password=request.form.get('password'))
        if connection.is_connected():
            return("connected")
        else:
            return("no")
    
    return render_template('extract.html',mysql_form=mysql_form)

@app.route('/transform')
@login_required
def transform():
    return render_template('transform.html')

@app.route('/transform/filter',methods=['GET','POST'])
@login_required
def filter():
    return render_template('filter.html',data=data)

@app.route('/load')
@login_required
def load():
    return render_template('load.html')


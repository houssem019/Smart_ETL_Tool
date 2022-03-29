from flask import Flask, redirect, render_template,session, url_for
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
from user.upload import UploadFileForm

@app.route('/')
def home():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('signup.html')

@app.route('/extract',methods=['GET','POST'])
@login_required
def extract():
    form=UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return redirect(url_for('filter'))
    return render_template('extract.html',form=form)

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


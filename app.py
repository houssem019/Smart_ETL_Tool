from flask import Flask, redirect, render_template,session
from functools import wraps
import pymongo
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key='intelligentetlprojecthoussemamanisupervisedbymaherheni'
app.config['SECRET_KEY'] = 'houssemamani'
app.config['UPLOAD_FOLDER'] = 'static/files'

client=pymongo.MongoClient('localhost', 27017)
db=client.etl


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
        return "File has been uploaded."
    return render_template('extract.html',form=form)

@app.route('/transform')
@login_required
def transform():
    return render_template('transform.html')

@app.route('/load')
@login_required
def load():
    return render_template('load.html')


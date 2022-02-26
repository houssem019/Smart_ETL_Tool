from fileinput import filename
from flask import Flask, redirect, render_template,session, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import pymongo
import gridfs
import os
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key='intelligentetlprojecthoussemamanisupervisedbymaherheni'
app.config['SECRET_KEY'] = 'houssemamani'
app.config['UPLOAD_FOLDER'] = 'static/files'


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
        uploaded_file = form.file.data # First grab the file
        files.put(uploaded_file,filename=uploaded_file.filename)
        local_location="E:/P2M/ETL/static/files/"+uploaded_file.filename
        downloaded_file=db.fs.files.find_one({'filename':uploaded_file.filename})
        outputdata=files.get(downloaded_file['_id']).read()
        output=open(local_location,"wb")
        output.write(outputdata)
        output.close()
        # file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return redirect(url_for('filter'))
    return render_template('extract.html',form=form)

@app.route('/transform')
@login_required
def transform():
    return render_template('transform.html')

@app.route('/transform/filter',methods=['GET','POST'])
@login_required
def filter():
    return render_template('filter.html')

@app.route('/load')
@login_required
def load():
    return render_template('load.html')


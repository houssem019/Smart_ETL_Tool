from flask import Flask, redirect, render_template,session
from functools import wraps
import pymongo

app=Flask(__name__)
app.secret_key='intelligentetlprojecthoussemamanisupervisedbymaherheni'

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

@app.route('/')
def home():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('signup.html')

@app.route('/extract')
@login_required
def extract():
    return render_template('extract.html')

@app.route('/transform')
@login_required
def transform():
    return render_template('transform.html')

@app.route('/load')
@login_required
def load():
    return render_template('load.html')


from flask import Flask, redirect, render_template,session, url_for
from functools import wraps
import pymongo
import gridfs
import os
from werkzeug.utils import secure_filename

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
        uploaded_file = form.file.data # First grab the file
        files.put(uploaded_file,filename=uploaded_file.filename)
        parent_dir="E:/P2M/ETL/static/files/"
        dir=session['user']['name']
        path=os.path.join(parent_dir,dir)
        if not os.path.exists(path):
            os.mkdir(path)
        local_location=path+"/"+uploaded_file.filename
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
    parent_dir="E:/P2M/ETL/static/files/"
    dir=session['user']['name']
    path=os.path.join(parent_dir,dir)
    files_list=os.listdir(path)
    print(type(files_list))
    return render_template('filter.html',files_list=files_list,len=len(files_list))

from filter import *

@app.route('/transform/filter/<string:name>')
@login_required
def function(name):
    scores=[]
    parent_dir_files="E:/P2M/ETL/static/files/"
    parent_dir_charts="E:/P2M/ETL/static/charts/"
    dir=session['user']['name']
    path_files=os.path.join(parent_dir_files,dir)
    path_charts=os.path.join(parent_dir_charts,dir)
    if not os.path.exists(path_charts):
            os.mkdir(path_charts)
    files_list=os.listdir(path_files)
    if name in files_list:
        name_chart=name[:-3]+"png"
        final_path_files=os.path.join(path_files,name)
        final_path_charts=os.path.join(path_charts,name_chart)
        path="charts/"+dir+"/"+name_chart
        df=read(final_path_files)
        X,y,discrete_features=preparation(df)
        if problem_type(y)==1:
            problem="Regression"
            scores=mi_scores_for_regression(X,y,discrete_features)
            plot_mi_scores(scores,final_path_charts)
        else:
            problem="Classification"
            scores=mi_scores_for_classification(X,y,discrete_features)
            plot_mi_scores(scores,final_path_charts)
        return render_template('csv.html',path=path,scores=scores,table=df.head().to_html(classes='dataframe'),filename=name[:-4],df=df,X=X,y=y,problem=problem)

@app.route('/load')
@login_required
def load():
    return render_template('load.html')


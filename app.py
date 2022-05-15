from flask import Flask, redirect,request, render_template,session, url_for, send_file
from functools import wraps
import pymongo
import gridfs
import os
import pickle

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
            os.makedirs(path)
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
    return render_template('filter.html',files_list=files_list,len=len(files_list))

from filter import *

@app.route('/transform/filter/<string:name>',methods=['GET','POST'])
@login_required
def function(name):
    parent_dir_files="E:/P2M/ETL/static/files/"
    parent_dir_filtred_files="E:/P2M/ETL/static/filtred_files/"
    parent_dir_charts="E:/P2M/ETL/static/charts/"
    dir=session['user']['name']
    path_files=os.path.join(parent_dir_files,dir)
    path_filtred_files=os.path.join(parent_dir_filtred_files,dir)
    path_charts=os.path.join(parent_dir_charts,dir)
    if not os.path.exists(path_charts):
            os.makedirs(path_charts)
    if not os.path.exists(path_filtred_files):
            os.makedirs(path_filtred_files)
    files_list=os.listdir(path_files)
    if name in files_list:
        name_chart=name[:-3]+"png"
        final_path_files=os.path.join(path_files,name)
        final_path_charts=os.path.join(path_charts,name_chart)
        path="charts/"+dir+"/"+name_chart
        df=read(final_path_files)
        X,y,discrete_features=preparation(df)
        outfile=path_filtred_files+"/"+name[:-3]+"_"+"scores"
        if problem_type(y)==1:
            problem="Regression"
            if not os.path.exists(outfile):
                scores=mi_scores_for_regression(X,y,discrete_features)
                plot_mi_scores(scores,final_path_charts)
                with open(outfile, 'wb') as fp:
                    pickle.dump(scores, fp)
        else:
            problem="Classification"
            if not os.path.exists(outfile):
                scores=mi_scores_for_classification(X,y,discrete_features)
                plot_mi_scores(scores,final_path_charts)
                with open(outfile, 'wb') as fp:
                    pickle.dump(scores, fp)
        with open (outfile, 'rb') as fp:
            scores = pickle.load(fp)
    return render_template('csv.html',path=path,length=len(scores),scores=scores,table=df.head().to_html(classes='dataframe'),filename=name[:-4],name=name,df=df,X=X,y=y,problem=problem)

@app.route('/transform/filter/<string:name>/done!',methods=['GET','POST'])
@login_required
def filtred(name):
    parent_dir_files="E:/P2M/ETL/static/files/"
    parent_dir_filtred_files="E:/P2M/ETL/static/filtred_files/"
    dir=session['user']['name']
    path_files=os.path.join(parent_dir_files,dir)
    path_filtred_files=os.path.join(parent_dir_filtred_files,dir)
    files_list=os.listdir(path_files)
    if name in files_list:
        final_path_files=os.path.join(path_files,name)
        path_filtred_file=path_filtred_files+"/"+"filtred_"+name
        outfile=path_filtred_files+"/"+name[:-3]+"_"+"scores"
        with open (outfile, 'rb') as fp:
            scores = pickle.load(fp)
    df=read(final_path_files)
    filter_features(df,scores,path_filtred_file)
    return redirect(request.referrer)

@app.route('/transform/filter/<string:name>/download',methods=['GET','POST'])
@login_required
def download_file(name):
    parent_dir_filtred_files="E:/P2M/ETL/static/filtred_files/"
    dir=session['user']['name']
    path_filtred_files=os.path.join(parent_dir_filtred_files,dir)
    path_filtred_file=path_filtred_files+"/"+"filtred_"+name
    return send_file(path_filtred_file,as_attachment=True)


@app.route('/load')
@login_required
def load():
    return render_template('load.html')


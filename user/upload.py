from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms import FileField, SubmitField,StringField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from wtforms import PasswordField

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
class My_SQL_Form(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    host = StringField('Host', validators=[DataRequired()])
    database = StringField('Database', validators=[DataRequired()])
    submit=SubmitField('Submit')

    

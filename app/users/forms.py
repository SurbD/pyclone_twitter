from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        Length(min=5, max=50), 
        Regexp(r"^[A-Za-z][A-Za-z0-9_.]*$", 0, 
               'Usernames must have only letters, numbers, dots or underscores')])

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            Length(min=5, max=50),
            Regexp(r"^[A-Za-z][A-Za-z]*$", 0, "Names must have only letters!"),
        ],
    )
    about_me = TextAreaField("About Me")
    location = StringField("Location")

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, EmailField,
                      SubmitField, BooleanField, DateField)
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=5, max=50),
        Regexp(r"^[A-Za-z][A-Za-z0-9_.]*$", 0, 
               'Usernames must have only letters, numbers, dots or underscores')])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if email.data.lower() == 'admin@blog.com':
            return False
            # raise ValidationError('Email already Registered!. Please try again')
        return True
        
    def validate_name(self, name):
        if name.data.lower() == 'admin':
            raise ValidationError("User with that name already exists. Please choose a different name")

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

# Test Forms
class LoginEmailForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Next')

class LoginPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class PostForm(FlaskForm):
    body = TextAreaField(
        "What's on your mind?", validators=[DataRequired(), Length(min=5, max=250)]
    )
    submit = SubmitField("Post")

    def validate_body(self, body):
        if not (5 <= len(body) <= 200):
            raise ValidationError("Character Length Error!!. Post \
            characters cannot be less than 5 and greater than 200 characters")

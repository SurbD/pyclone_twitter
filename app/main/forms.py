from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class PostForm(FlaskForm):
    body = TextAreaField(
        "What's on your mind?", validators=[DataRequired(), Length(min=5, max=250)]
    )
    submit = SubmitField("Post")

    # def validate_body(self, body):
    #     if not (5 <= len(body.data) <= 250):
    #         raise ValidationError("Character Length Error! \
    #         Field must be between 5 and 250 characters long")

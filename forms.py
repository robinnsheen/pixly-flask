from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class PictureAddForm(FlaskForm):
    """Form for adding pictures."""

    picture = StringField('Picture', validators=[DataRequired()])


class PictureAddForm(FlaskForm):
    """Form for editing pictures."""

    picture = StringField('Picture', validators=[DataRequired()])

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms import validators


class PictureAddForm(FlaskForm):
    """Form for adding pictures."""
    name = StringField('Name')
    file = FileField('Image File')

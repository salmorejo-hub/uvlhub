from flask_wtf import FlaskForm
from wtforms import SubmitField


class APIForm(FlaskForm):
    submit = SubmitField('Save API')

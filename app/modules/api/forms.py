from flask_wtf import FlaskForm
from wtforms import SubmitField


class ApiForm(FlaskForm):
    submit = SubmitField('Save api')

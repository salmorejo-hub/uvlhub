from flask_wtf import FlaskForm
from wtforms import SubmitField


class DiscordbotForm(FlaskForm):
    submit = SubmitField('Save discordbot')

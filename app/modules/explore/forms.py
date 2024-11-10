from flask_wtf import FlaskForm
from wtforms import SubmitField


class ExploreForm(FlaskForm):
    submit = SubmitField('Submit')


class ExploreUvl(FlaskForm):
    submit = SubmitField('Submit')

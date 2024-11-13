from flask_wtf import FlaskForm
from wtforms import SubmitField


class ExploreFormUvl(FlaskForm):
    submit = SubmitField('Submit')

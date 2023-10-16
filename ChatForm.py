from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length

class ChatForm(FlaskForm):
    content = StringField('Talk to our fine tuned chat bot?', validators=[DataRequired(), Length(5, 40)])
    submit = SubmitField('Submit')

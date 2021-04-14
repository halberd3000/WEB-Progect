from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):
    name = StringField('Название темы', validators=[DataRequired()])
    text = TextAreaField("Содержание темы", validators=[DataRequired()])
    submit = SubmitField('Применить')

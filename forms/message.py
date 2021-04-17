# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    text = TextAreaField("Текст сообщения", validators=[DataRequired()])
    submit = SubmitField('Применить')
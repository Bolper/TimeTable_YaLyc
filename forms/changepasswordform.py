from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Введите старый пароль"})
    new_password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Введите новый пароль"})
    submit = SubmitField('Подтвердить')

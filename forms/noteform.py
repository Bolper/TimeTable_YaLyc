from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class NoteForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()], render_kw={"placeholder": "Введите название"})
    description = StringField('Описание', render_kw={"placeholder": "Введите описание"})
    position = StringField('Место', render_kw={"placeholder": "Введите место"})
    starts = DateTimeField('Начало', validators=[DataRequired()],
                           render_kw={"placeholder": "Год-Месяц-День час:минута:секунда"})
    ends = DateTimeField('Конец', validators=[DataRequired()],
                         render_kw={"placeholder": "Год-Месяц-День час:минута:секунда"})
    is_finished = BooleanField('Выполнено')
    submit = SubmitField('Создать')

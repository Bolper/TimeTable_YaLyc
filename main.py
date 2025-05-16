import datetime

from flask import Flask, request, url_for, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

from data import __db_session as db_session

db_session.global_init("db/database.sqlite")

from data.users import User
from data.notes import Note
from api import notes as notes_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

from forms import LoginForm, RegisterForm, NoteForm


@login_manager.user_loader
def load_user(user_id: id) -> User | None:
    return db_session.create_session().get(User, user_id)


@app.route('/index')
@app.route('/')
def index():
    params = {
        'title': 'Домашняя страница',
    }
    return render_template('index.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/show/notes")
        return render_template('_base_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('_base_form.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('_base_form.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('_base_form.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def add_notes():
    form = NoteForm()
    if request.method == 'GET':
        return render_template('_base_form.html', title='Adding job', form=form)
    db_sess = db_session.create_session()
    if form.validate_on_submit() and request.method == 'POST':
        note = Note(
            user_id=current_user.id
        )
        form.populate_obj(note)
        db_sess.merge(note)
        db_sess.commit()
        return redirect('/show/notes')
    return render_template('_base_form.html', title='Adding job', form=form)


@app.route('/show/notes')
@login_required
def show_notes():
    db_sess = db_session.create_session()
    notes = db_sess.query(Note).filter(current_user.id == Note.user_id)  # доделать
    params = {
        'title': 'Notes',
        'notes': notes
    }
    return render_template('notes.html', **params)


@app.errorhandler(404)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/notes/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_news(_id):
    db_sess = db_session.create_session()
    note = db_sess.get(Note, _id)
    if note is None:
        abort(404)
    form = NoteForm()
    if request.method == "GET":
        return render_template('_base_form.html', title='Editing job', form=form)
    if form.validate_on_submit() and request.method == 'POST':
        form.populate_obj(note)
        db_sess.merge(note)
        db_sess.commit()
        return redirect('/show/notes')


@app.route('/notes_delete/<int:_id>')
@login_required
def jobs_delete(_id):
    db_sess = db_session.create_session()
    note = db_sess.get(Note, _id)
    if note is None:
        abort(404)
    db_sess.delete(note)
    db_sess.commit()
    return redirect('/show/notes')


if __name__ == '__main__':
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
    app.register_blueprint(notes_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
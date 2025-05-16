from flask import Blueprint, jsonify, request, make_response

from data import __db_session as db_session
from data.notes import Note
from data.users import User

blueprint = Blueprint(
    'notes_api',
    __name__,
    template_folder='templates'
)

NOTE_ATTRS = (
    'id', 'name', 'description', 'position', 'starts', 'ends',
    'is_finished')


@blueprint.route('/api/<string:_login>/<string:_password>/notes')
def get_notes(_login: str, _password: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == _login).first()
    if not user.check_password(_password):
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    notes = db_sess.query(Note).filter(User.id == Note.user_id)
    return jsonify({
        'notes': [note.to_dict(only=NOTE_ATTRS) for note in notes]
    })


@blueprint.route('/api/<string:_login>/<string:_password>/notes/<int:_id>', methods=['GET'])
def get_one_note(_login: str, _password: str, _id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == _login).first()
    if not user.check_password(_password):
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    note = db_sess.query(Note).get(_id)
    return jsonify({
        'notes': note.to_dict(only=NOTE_ATTRS)
    })


@blueprint.route('/api/<string:_login>/<string:_password>/notes/<int:_id>', methods=['DELETE'])
def delete_note(_login: str, _password: str, _id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == _login).first()
    if not user.check_password(_password):
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    note = db_sess.query(Note).get(_id)
    db_sess.delete(note)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/<string:_login>/<string:_password>/notes', methods=['POST'])
def create_note(_login: str, _password: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == _login).first()
    if not user.check_password(_password):
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json
                 for key in ['name', 'description', 'position', 'starts', 'ends', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    note = Note(
        name=request.json['name'],
        description = request.json['description'],
        position = request.json['position'],
        starts = request.json['starts'],
        ends = request.json['ends'],
        is_finished = request.json['is_finished'],
        user_id = user.id
    )
    db_sess.merge(note)
    db_sess.commit()
    return jsonify({'id': note.id})

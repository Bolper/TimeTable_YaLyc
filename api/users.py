from flask import Blueprint, jsonify, request, make_response

from data import __db_session as db_session
from data.users import User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)

USER_ATTRS = (
    'id', 'surname', 'name', 'age', 'address', 'email')


@blueprint.route('/api/<string:_login>/<string:_password>/user', methods=['GET'])
def get_user(_login: str, _password: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == _login).first()
    if not user.check_password(_password):
        return make_response(jsonify({'error': 'Unauthorized'}), 403)
    return jsonify({
        'user': user.to_dict(only=USER_ATTRS)
    })


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    db_sess = db_session.create_session()
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json
                 for key in ['surname', 'name', 'age', 'address', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        address=request.json['starts'],
        email=request.json['email']
    )
    user.set_password(request.json['password'], )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})

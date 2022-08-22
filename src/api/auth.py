import json
from http import HTTPStatus
from operator import itemgetter

from flask import (
    Blueprint, request,
)

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from db.config import db, token_storage
from db.models import User
from service.account import AccountService
from service.exceptions import UserAlreadyExists, UserDoesntExists, WrongPassword, EditUserException
from settings import settings

auth_api = Blueprint('auth', __name__, url_prefix='/auth')
account_service = AccountService(db)


@auth_api.route('/register', methods=['POST'])
def register():
    user_name, password, email = itemgetter('login', 'password', 'email')(request.args)
    try:
        account_service.register(user_name, password, email)
    except UserAlreadyExists:
        pass
    return {'msg': 'Account created'}, HTTPStatus.OK


@auth_api.route('/login', methods=['POST'])
def login():
    user_name, password = itemgetter('login', 'password')(request.args)
    try:
        user = account_service.login(login=user_name, password=password)
    except UserDoesntExists:
        return {'msg': 'Authorization Error'}, HTTPStatus.UNAUTHORIZED
    except WrongPassword:
        return {'msg': 'Authorization Error'}, HTTPStatus.UNAUTHORIZED
    tokens = _authorize_user(user, request.headers['User-Agent'])
    return tokens, HTTPStatus.OK


@auth_api.route('/logout')
def logout():
    access_token = decode_token(request.headers['Access-Token'])
    refresh_token = decode_token(request.headers['Refresh-Token'])
    token_storage.set_value(access_token['jti'], '', time_to_leave=settings.jwt.access_token_expire_time)
    token_storage.set_value(refresh_token['jti'], '', time_to_leave=settings.jwt.refresh_token_expire_time)
    return {'msg': 'Successfully logged out'}, HTTPStatus.OK


@auth_api.route('/login-history')
@jwt_required()
def login_history():
    user_id = get_jwt_identity()
    user_sessions = account_service.get_user_sessions(user_id)

    return str([{key: str(user_session.__dict__[key]) for key in ['user_id', 'created_at']} for user_session in
                user_sessions]), HTTPStatus.OK


@auth_api.route('/edit-user', methods=['POST'])
@jwt_required()
def edit_user():
    user_id = get_jwt_identity()
    user_name = request.form.get('login')
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        account_service.edit_user(user_id, user_name, email, password)
    except EditUserException:
        return {'msg': 'Edit user error'}, HTTPStatus.BAD_REQUEST
    return {'msg': 'Edit user success'}, HTTPStatus.OK


@auth_api.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    refresh_token_jti = get_jwt()['jti']
    token_storage.set_value(refresh_token_jti, '', time_to_leave=settings.jwt.refresh_token_expire_time)
    return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


def _authorize_user(user: User, user_agent: str) -> dict:
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    account_service.register_user_session(user.id, user_agent)
    return {'access_token': access_token, 'refresh_token': refresh_token}

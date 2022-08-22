from http import HTTPStatus

from flask import (
    Blueprint, request,
)

from flask_jwt_extended import (
    jwt_required,
)

from db.config import db
from permissions import role_required
from service.exceptions import RoleAlreadyExists, RoleDoesntExists, RelationDoesntExists
from service.roles import RoleService

role_api = Blueprint('role', __name__, url_prefix='/role')
role_service = RoleService(db)


@role_api.route('', methods=['GET', 'PUT', 'POST', 'DELETE'])
@jwt_required()
@role_required('admin')
def role():
    if request.method == 'GET':
        roles =  [r.name for r in role_service.get_all_roles()]
        return {'roles': str(roles)}, HTTPStatus.OK
    if request.method == 'PUT':
        try:
            role_service.edit_role(request.form.get('name'), request.form.get('new_name'), request.form.get('new_description'))
        except RoleAlreadyExists:
            return {'msg': 'Role already exists'}, HTTPStatus.CONFLICT
        return {'msg': 'Role edited'}, HTTPStatus.OK
    if request.method == 'POST':
        try:
            role = role_service.create_role(
                name=request.form.get('name'),
                description=request.form.get('description'),
            )
        except RoleAlreadyExists:
            return {'msg': 'Role already exists'}, HTTPStatus.CONFLICT
        role_data = {
            'id': role.id,
            'name': role.name,
            'description': role.description,
        }
        return role_data, HTTPStatus.OK
    if request.method == 'DELETE':
        try:
            role_service.delete_role(request.args['name'])
        except RoleDoesntExists:
            return {'msg': 'Role not found'}, HTTPStatus.NOT_FOUND
        return {'msg': 'Role deleted'}, HTTPStatus.OK


@role_api.route('/user', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
@role_required('admin')
def user_role():
    if request.method == 'GET':
        name = request.args['login']
        roles = role_service.get_user_roles(login=name)
        return {'roles': [role.name for role in roles]}, HTTPStatus.OK
    if request.method == 'POST':
        try:
            role_service.set_user_role(request.form.get('login'), request.form.get('role_name'))
        except RelationDoesntExists:
            return {'msg': 'Role not found'}, HTTPStatus.NOT_FOUND
        return {'msg': 'Role set'}, HTTPStatus.OK
    if request.method == 'DELETE':
        try:
            role_service.delete_user_role(request.form.get('login'), request.form.get('role_name'))
        except RelationDoesntExists:
            return {'msg': 'Role not found'}, HTTPStatus.NOT_FOUND
        return {'msg': 'Role removed'}, HTTPStatus.OK

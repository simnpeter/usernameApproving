from flask import Blueprint, request, jsonify
from services.user_service import register_user, login_user, get_all_users, update_user_approval, predict
user_routes = Blueprint('user_routes', __name__)
from cerberus import Validator

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    rules = {
    'username': {'type': 'string', 'minlength': 4, 'required': True},
    'password': {'type': 'string', 'required': True}
    }
    validator = Validator(rules)

    if not validator.validate(data):
        return jsonify(validator.errors), 402

    username = data['username']
    password = data['password']

    approved_value = predict(username)

    if approved_value is not None:
        response, status = register_user(username, password, approved_value)
        return jsonify(response), status
    else :
        return jsonify(approved_value), 400

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    rules = {
    'username': {'type': 'string', 'minlength': 4, 'required': True},
    'password': {'type': 'string', 'required': True}
    }
    validator = Validator(rules)

    if not validator.validate(data):
        return jsonify(validator.errors), 400

    username = data['username']
    password = data['password']

    user, status = login_user(username, password)
    if status == 200:
        return jsonify({"user": user}), status
    else:
        return jsonify({"message": user["message"]}), status

@user_routes.route('/admin', methods=['GET'])
def get_users():
    users, status = get_all_users()
    return jsonify({"users": users}), status

@user_routes.route('/admin', methods=['PATCH'])
def approve_manual():
    data = request.get_json()

    rules = {
    'user_id': {'type': 'string', 'required':True},
    'approved': {'type': 'boolean', 'required': True}
    }
    validator = Validator(rules)

    if not validator.validate(data):
        return jsonify(validator.errors), 400

    user_id = data.get('user_id')
    approved = data.get('approved')

    response, status = update_user_approval(user_id, approved)
    return jsonify(response), status

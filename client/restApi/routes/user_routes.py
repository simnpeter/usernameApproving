# routes/user_routes.py
from flask import Blueprint, request, jsonify, current_app
from models.user import User
import jwt
import datetime
import requests
from services.user_service import register_user, login_user, get_all_users, update_user_approval
from config import SECRET_KEY

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Hívás a predikciós API-hoz
    approval_response = requests.post('http://127.0.0.1:5000/predict', json={"name": username})
    approved_value = approval_response.json()['approved']

    # Felhasználó regisztrálása
    response, status = register_user(username, password, approved_value)
    return jsonify(response), status

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Felhasználó bejelentkezése
    user, status = login_user(username, password)
    if status == 200:
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token}), 200
    return jsonify(user), status

@user_routes.route('/users', methods=['GET'])
def get_users():
    # Felhasználók lekérése
    users, status = get_all_users()
    serialized_users = [user.to_json() for user in users]
    return jsonify({"users": serialized_users}), status

@user_routes.route('/users', methods=['PATCH'])
def approve_manual():
    data = request.get_json()
    user_id = data.get('user_id')
    approved = data.get('approved')

    if not user_id or approved is None:
        return jsonify({'error': 'user_id and approved are required'}), 400

    # Felhasználó frissítése
    response, status = update_user_approval(user_id, approved)
    
    if status == 200:
        name = User.objects(id=user_id).first().username
        requests.post('http://127.0.0.1:5000/add_name', json={"name": name, "label": approved})

    return jsonify(response), status

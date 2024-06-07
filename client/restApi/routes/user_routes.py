# routes/user_routes.py
from flask import Blueprint, request, jsonify, current_app
from models.user import User
import jwt
import datetime
import requests
from flask_cors import  cross_origin
from services.user_service import register_user, login_user, get_all_users, update_user_approval, predict
from config import SECRET_KEY

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Hívás a predikciós API-hoz
    approved_value = predict(username)

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
        return jsonify({"user": user}), status
    else:
        return jsonify({"message": user["message"]}), status

@user_routes.route('/users', methods=['GET'])
def get_users():
    # Felhasználók lekérése
    users, status = get_all_users()
    return jsonify({"users": users}), status

@user_routes.route('/users', methods=['PATCH'])
def approve_manual():
    data = request.get_json()
    user_id = data.get('user_id')
    approved = data.get('approved')

    if not user_id or approved is None:
        return jsonify({'error': 'user_id and approved are required'}), 400

    # Felhasználó frissítése
    response, status = update_user_approval(user_id, approved)
    return jsonify(response), status

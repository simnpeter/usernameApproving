# services/user_service.py
from models.user import User
from datetime import datetime
import bcrypt
import requests
import json
from bson import ObjectId, json_util

def register_user(username, password, approved):
    if User.objects(username=username).first():
        return {"message": "User already exists"}, 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password, approved_ai=approved)
    user.save()
    return {"message": "User registered successfully",
        "approved_ai": approved}, 201

def login_user(username, password):
    user = User.objects(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"message": "Invalid credentials"}, 401
    if user.approved_human is False or (user.approved_ai is False and user.approved_human is  None):
        return {"message": "Username is not approved"}, 401
    user_dict = user.to_mongo().to_dict()

    # Convert ObjectId to string
    user_dict['_id'] = str(user_dict['_id'])

    # Convert datetime object to ISO format string for JSON serialization
    if 'modified' in user_dict:
        user_dict['modified'] = user_dict['modified'].isoformat()

    return user_dict, 200

def get_all_users():
    users = User.objects(is_admin=False).exclude('password')
    
    users_list = []
    for user in users:
        user_dict = user.to_mongo().to_dict()

        # Convert ObjectId to string
        user_dict['_id'] = str(user_dict['_id'])

        # Convert datetime object to ISO format string for JSON serialization
        if 'modified' in user_dict:
            user_dict['modified'] = user_dict['modified'].isoformat()
        
        users_list.append(user_dict)

    # Sort by approved_human and modified
    users_list.sort(key=lambda user: (
        -1 if user['approved_human'] is None else (1 if not user['approved_human'] else 2),
        user['modified']
    ))


    return users_list, 200

def update_user_approval(user_id, approved):
    user = User.objects(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

    user.approved_human = approved
    user.modified = datetime.now()
    user.save()
    return {"message": "User updated successfully"}, 200

def predict(name):
    approval_response = requests.post('http://127.0.0.1:5000/predict', json={"username": name})

    if approval_response.status_code is not 200:
        return  None
    
    approved_value = approval_response.json()['approved']

    return approved_value

    
    

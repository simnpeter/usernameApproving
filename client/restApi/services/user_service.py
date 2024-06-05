# services/user_service.py
from models.user import User
from datetime import datetime
import bcrypt
import json
from bson import ObjectId, json_util

def register_user(username, password, approved):
    if User.objects(username=username).first():
        return {"message": "User already exists"}, 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password, approved=approved)
    user.save()
    return {"message": "User registered successfully"}, 201

def login_user(username, password):
    user = User.objects(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"message": "Invalid credentials"}, 401

    return user, 200

def get_all_users():
    users = User.objects.exclude('password')
    
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
    users_list.sort(key=lambda x: (x['approved_human'], x['modified']))

    return users_list, 200

def update_user_approval(user_id, approved):
    user = User.objects(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

    user.approved_human = approved
    user.modified = datetime.now()
    user.save()
    return {"message": "User updated successfully"}, 200

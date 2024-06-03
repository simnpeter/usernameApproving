# services/user_service.py
from models.user import User
import bcrypt

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
    
    return users, 200

def update_user_approval(user_id, approved):
    user = User.objects(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

    user.ApprovedHuman = approved
    user.save()
    return {"message": "User updated successfully"}, 200

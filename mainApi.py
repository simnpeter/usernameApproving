from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
import requests
import certifi
import bcrypt
import jwt
import json
from bson import ObjectId, json_util
import datetime
from config import MONGO_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.get_database()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']


    if db.user.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    approval_response = requests.post('http://127.0.0.1:5000/predict', json={"name": username})
    approved_value = approval_response.json()['approved']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.user.insert_one({"username": username, "password": hashed_password, "ApprovedAi":approved_value, "ApprovedHuman":None})
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = db.users.find_one({"username": username})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({"token": token}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = db.user.find({}, {"password": 0})
    # Konvertáljuk az ObjectId-t stringgé
    serialized_users = [json.loads(json_util.dumps(user)) for user in users]
    return jsonify({"users": serialized_users}), 200

@app.route('/users', methods=['PATCH'])
def approve_manual():
    try:
        # Adatok kinyerése a kérésből
        data = request.get_json()
        user_id = data.get('user_id')
        approved = data.get('approved')

        if not user_id or approved is None:
            return jsonify({'error': 'user_id and approved are required'}), 400

        users_collection = db.get_collection('users')

        try:
            user_id = ObjectId(user_id)
        except:
            return jsonify({"error": "Invalid user_id format"}), 400
        # Felhasználó keresése és frissítése
        result = db.user.update_one({"_id": user_id}, {"$set": {"ApprovedHuman": approved}})

        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404
        
        name = db.user.find_one({"_id": user_id})

        if name is None:
            return jsonify({"error": "User not found"}), 404

        response = requests.post('http://127.0.0.1:5000/add_name', json={"name": name['username'], "label":approved})

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001,debug=True)

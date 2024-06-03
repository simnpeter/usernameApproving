# routes/user_data_routes.py
from flask import Blueprint, request, jsonify
from services.user_data_service import add_name_to_db, predict

user_data_routes = Blueprint('user_data_routes', __name__)

@user_data_routes.route('/add_name', methods=['POST'])
def add_name():
    data = request.get_json()
    name = data['name']
    label = data['label']
    
    response, status = add_name_to_db(name, label)
    return jsonify(response), status

@user_data_routes.route('/predict', methods=['POST'])
def predict_route():
    data = request.get_json()
    name = data['name']
    
    response, status = predict(name)
    return jsonify(response), status

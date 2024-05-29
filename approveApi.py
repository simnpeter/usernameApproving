from flask import Flask, request, jsonify
#from sklearn.linear_model import RandomForestClassifier
import numpy as np
from pymongo.mongo_client import MongoClient
import certifi
from config import MONGO_URI

app = Flask(__name__)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.get_database()
# Inicializáljuk a modellt
#model = RandomForestClassifier()
# Inicializáljuk az adattárat és a küszöböt

threshold = 20

@app.route('/add_name', methods=['POST'])
def add_name():
    global new_names, new_labels
    data = request.get_json()
    name = data['name']
    label = data['label']  

    db.newUsernames.insert_one({"username": name, "label": label})

    new_data = list(db.newUsernames.find({}))
    new_names = [item['username'] for item in new_data]
    new_labels = [item['label'] for item in new_data]

    if len(new_names) >= threshold:
        # Átalakítjuk a neveket feature-ekké (egyszerű példa: string hossza)
        X_new = new_names
        y_new = new_labels
        
        # Frissítjük a modellt az új adatokkal
        #model.partial_fit(X_new, y_new)

        db.newUsernames.delete_many({})

        return jsonify({"message": "Model updated with new data"}), 200
    else:
        return jsonify({"message": "Name added, but not enough data to retrain"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    name = data['name']
    
    # Átalakítjuk a nevet feature-é
    X = name
    
    # Predikciót végzünk a modellel
    #prediction = model.predict(X)
    
    return jsonify({"approved": True}), 200

if __name__ == '__main__':
    app.run(port=5000,debug=True)

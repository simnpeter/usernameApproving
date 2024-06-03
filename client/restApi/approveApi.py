# app.py
from flask import Flask
from mongoengine import connect
from routes.user_data_routes import user_data_routes
from config import MONGO_URI, TLS_CA_FILE

app = Flask(__name__)

# MongoDB csatlakozás
connect(host=MONGO_URI, tlsCAFile=TLS_CA_FILE)

# Útvonalak regisztrálása
app.register_blueprint(user_data_routes)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# app.py
from flask import Flask
from mongoengine import connect
from routes.user_routes import user_routes
from config import MONGO_URI, SECRET_KEY, TLS_CA_FILE
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = SECRET_KEY

# MongoDB csatlakozás
connect(host=MONGO_URI, tlsCAFile=TLS_CA_FILE)

# Útvonalak regisztrálása
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

# app.py
from flask import Flask
from mongoengine import connect
from routes.user_routes import user_routes
from config import MONGO_URI, SECRET_KEY, TLS_CA_FILE

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# MongoDB csatlakozás
connect(host=MONGO_URI, tlsCAFile=TLS_CA_FILE)

# Útvonalak regisztrálása
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

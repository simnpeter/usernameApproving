from pymongo.mongo_client import MongoClient
import certifi
from config import MONGO_URI



# Create a new client and connect to the server with the CA file for SSL verification
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

# Get the database
db = client.get_database()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print("Connected to database:", db.name)
except Exception as e:
    print(e)

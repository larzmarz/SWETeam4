from decouple import config
from pymongo import MongoClient
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

MONGODB_URI = 'mongodb+srv://SWE4:SWET4@cluster0.ln7pqzu.mongodb.net/geek_text_db'
client = MongoClient(MONGODB_URI)
db = client['geek_text_db']
# <collection name>_collection = db['<collection name>']

# Routes Here

if __name__ == '__main__':
    app.run(debug=True)
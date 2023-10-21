from decouple import config
from pymongo import MongoClient, DESCENDING
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

MONGODB_URI = config('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['geek_text_db']
# <collection name>_collection = db['<collection name>']

# Routes Here

if __name__ == '__main__':
    app.run(debug=True)
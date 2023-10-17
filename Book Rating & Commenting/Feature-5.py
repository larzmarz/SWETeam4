from flask import Flask, jsonify, request, abort
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['geek_text_db']

#Code Here

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request
from pymongo import MongoClient
import mysql.connector

app = Flask(__name__)

users = {}  # A simple in-memory database for demonstration purposes
credit_cards = {}  # Another in-memory database for credit cards


# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['geektext']
books_collection = db['profile']


conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="geektext"
)

cursor = conn.cursor()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    if username in users:
        return jsonify({"message": "Username already exists"}), 400
    users[username] = data
    return '', 201  # 201 means "Created"


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = users.get(username)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user)


@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    if username not in users:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    # Prevent updating email
    data.pop('email_address', None)
    users[username].update(data)
    return '', 200  # 200 means "OK"


@app.route('/users/<username>/credit-card', methods=['POST'])
def create_credit_card(username):
    if username not in users:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    credit_cards[username] = data
    return '', 201


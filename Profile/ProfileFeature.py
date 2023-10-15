from flask import Flask, jsonify, request
from pymongo import MongoClient
import mysql.connector

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['geektext']
users_collection = db['usernames']  # Using a MongoDB collection for users
credit_cards_collection = db['credit_cards']  # Using a MongoDB collection for credit cards

# MySQL setup
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="SWETeam4"
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


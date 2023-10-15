from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB setup
uri = "mongodb+srv://laurys3577:geektext@sweteam4.cebkbje.mongodb.net/"

client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['geek_text']
users_collection = db['users']  # Using a MongoDB collection for users
credit_cards_collection = db['credit_cards']  # Using a MongoDB collection for credit cards

# Creating a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    users_collection.insert_one(data)
    return '', 201  # 201 means "Created"

# Retrieving a specific user
@app.route('/users/<string:username>', methods=['GET'])
def get_user(username):
    user = users_collection.find_one({'username': username})
    if user:
        # Convert ObjectId to string because it's not JSON serializable
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

# updating user profile
@app.route('/users/<string:username>', methods=['PUT'])
def update_user(username):
    data = request.json

    # Check if the user exists
    user = users_collection.find_one({'username': username})
    if not user:
        return jsonify({"message": "User not found"}), 404
    # Remove the email field from the incoming data to ensure it's not updated
    data.pop('email', None)
    # Update the user's details
    users_collection.update_one({'username': username}, {"$set": data})
    return jsonify({"message": "User updated successfully"}), 200


@app.route('/addCreditCard', methods=['POST'])
def add_credit_card():
    data = request.json
    username = data['username']
    credit_card = data['creditCard']

    user = users_collection.find_one({'username': username})

    if user:
        credit_card['userId'] = user['_id']
        credit_cards_collection.insert_one(credit_card)
        return jsonify({'message': 'Credit card added successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


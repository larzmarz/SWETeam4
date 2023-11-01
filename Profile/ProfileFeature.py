from flask import Flask, jsonify, request, abort
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['geek_text_db']
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
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

# updating user profile
@app.route('/users/<string:username>', methods=['PUT','PATCH'])
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

if __name__ == '__main__':
    app.run(debug=True)
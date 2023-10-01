from flask import Flask, jsonify, request
from pymongo import MongoClient
import mysql.connector

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['geektext']
books_collection = db['books']

# MySQL setup
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="geektext"
)
cursor = conn.cursor()

@app.route('/api/books/genre', methods=['GET'])
def get_books_by_genre():
    genre = request.args.get('genre')
    books = list(books_collection.find({"genre": genre}))
    return jsonify(books), 200

@app.route('/api/books/top-sellers', methods=['GET'])
def get_top_sellers():
    books = list(books_collection.find().sort("copiesSold", -1).limit(10))
    return jsonify(books), 200

@app.route('/api/books/rating', methods=['GET'])
def get_books_by_rating():
    rating = float(request.args.get('rating'))
    books = list(books_collection.find({"rating": {"$gte": rating}}))
    return jsonify(books), 200

@app.route('/api/books/discount', methods=['PUT'])
def discount_books_by_publisher():
    discount_percent = int(request.args.get('discount_percent'))
    publisher = request.args.get('publisher')

    # Update MongoDB
    books = books_collection.find({"publisher": publisher})
    for book in books:
        new_price = book["price"] * (1 - discount_percent/100)
        books_collection.update_one({"_id": book["_id"]}, {"$set": {"price": new_price}})

    # Update MySQL
    cursor.execute("UPDATE publishers SET DiscountPercent = %s WHERE Name = %s", (discount_percent, publisher))
    conn.commit()

    return jsonify({"message": "Discount applied successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)

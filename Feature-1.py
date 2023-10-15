from flask import Flask, jsonify, request, abort
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['geek_text_db']
books_collection = db['books']

@app.route('/books/genre/<genre>', methods=['GET'])
def get_books_by_genre(genre):
    try:
        books = list(books_collection.find({"genre": genre}))
        if not books:
            return jsonify({"error": "No books found for this genre"}), 404
        for book in books:
            book['_id'] = str(book['_id'])
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/books/top-sellers', methods=['GET'])
def get_top_sellers():
    try:
        books = list(books_collection.find().sort("copies_sold", DESCENDING).limit(10))
        if not books:
            return jsonify({"error": "No books found in the database"}), 404
        for book in books:
            book['_id'] = str(book['_id'])
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/books/rating/<float:rating>', methods=['GET'])
def get_books_by_rating(rating):
    try:
        books = list(books_collection.find({"rating": {"$gte": rating}}))
        if not books:
            return jsonify({"error": "No books found for this rating or higher"}), 404
        for book in books:
            book['_id'] = str(book['_id'])
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/books/discount', methods=['PUT', 'PATCH'])
def discount_books_by_publisher():
    try:
        discount_percent = float(request.json.get('discount_percent', 0))
        publisher = request.json.get('publisher', "")
        
        if not publisher or discount_percent <= 0:
            abort(400, description="Invalid input data")
        
        books = books_collection.find({"publisher": publisher})
        if not books:
            return jsonify({"error": "No books found for this publisher"}), 404
        
        for book in books:
            new_price = book['price'] * (1 - discount_percent/100)
            books_collection.update_one({"_id": book['_id']}, {"$set": {"price": new_price}})
        
        return jsonify({"message": "Prices updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

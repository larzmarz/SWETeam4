from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
<<<<<<< Updated upstream
from decouple import config
=======
from decouple import config 
>>>>>>> Stashed changes
app = Flask(__name__)

MONGODB_URI = config('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['geek_text_db']
books_collection = db['books']

# API endpoint to create a rating for a book
@app.route('/rate-book', methods=['POST'])
def rate_book():
    data = request.get_json()
    book_id = data['book_id']
    user_id = data['user_id']
    rating = data['rating']
    datestamp = datetime.now()
    
    # Check if the user has already rated the book
    book = books_collection.find_one({"_id": book_id})
    ratings = book.get('ratings', [])
    existing_rating = next((r for r in ratings if r['user_id'] == user_id), None)
    
    if existing_rating:
        # Update the existing rating
        existing_rating['rating'] = rating
        existing_rating['datestamp'] = datestamp
        books_collection.update_one({"_id": book_id}, {"$set": {"ratings": ratings}})
        return jsonify({"message": "Rating updated successfully"}), 200
    else:
        # Save the new rating to MongoDB
        books_collection.update_one({"_id": book_id}, {"$push": {"ratings": {"user_id": user_id, "rating": rating, "datestamp": datestamp}}})
        return jsonify({"message": "Rating added successfully"}), 200

# API endpoint to create a comment for a book
@app.route('/comment-book', methods=['POST'])
def comment_book():
    data = request.get_json()
    book_id = data['book_id']
    user_id = data['user_id']
    comment = data['comment']
    datestamp = datetime.now()

    # Save the comment to MongoDB
    books_collection.update_one({"_id": book_id}, {"$push": {"comments": {"user_id": user_id, "comment": comment, "datestamp": datestamp}}})
    return jsonify({"message": "Comment added successfully"}), 200

# API endpoint to retrieve comments for a book
@app.route('/get-comments/<string:book_id>', methods=['GET'])
def get_comments(book_id):
    book = books_collection.find_one({"_id": book_id})
    comments = book.get('comments', [])
    return jsonify(comments), 200

# API endpoint to retrieve average rating for a book
@app.route('/get-average-rating/<string:book_id>', methods=['GET'])
def get_average_rating(book_id):
    book = books_collection.find_one({"_id": book_id})
    ratings = book.get('ratings', [])
    if not ratings:
        return jsonify({"average_rating": 0}), 200
    total_ratings = sum([rating['rating'] for rating in ratings])
    average_rating = total_ratings / len(ratings)
    return jsonify({"average_rating": average_rating}), 200

if __name__ == '__main__':
    app.run(debug=True)

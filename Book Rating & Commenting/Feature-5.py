from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
app = Flask(__name__)

MONGODB_URI = 'mongodb+srv://SWE4:SWET4@cluster0.ln7pqzu.mongodb.net/geek_text_db'
db = client['geektext']
books_collection = db['books']

# API endpoint to create a rating for a book
@app.route('/rate-book', methods=['POST'])
def rate_book():
    data = request.get_json()

    # Extract data from the request
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    rating = data.get('rating')

    # Check if the required data is present
    if not (book_id and user_id and rating):
        abort(400, description="Missing required parameters")

    # Check if the book exists in the collection
    book = books_collection.find_one({"_id": ObjectId(book_id)})

    if book is None:
        abort(404, description=f"Book with ID {book_id} not found")

    # Get existing ratings for the book
    ratings = book.get('ratings', [])

    # Check if the user has already rated the book
    existing_rating = next((r for r in ratings if r['user_id'] == user_id), None)

    if existing_rating:
        # Update the existing rating
        existing_rating['rating'] = rating
        existing_rating['datestamp'] = datetime.now()
    else:
        # Add a new rating
        new_rating = {"user_id": user_id, "rating": rating, "datestamp": datetime.now()}
        ratings.append(new_rating)

    # Update the ratings in the MongoDB collection
    books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"ratings": ratings}})

    if existing_rating:
        return jsonify({"message": "Rating updated successfully"}), 200
    else:
        return jsonify({"message": "Rating added successfully"}), 200



# API endpoint to create a comment for a book
@app.route('/comment-book', methods=['POST'])
def comment_book():
    data = request.get_json()

    # Extract data from the request
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    comment = data.get('comment')

    if not (book_id and user_id and comment):
        abort(400, description="Missing required parameters")

    # Save the comment to MongoDB
    books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$push": {"comments": {"user_id": user_id, "comment": comment, "datestamp": datetime.now()}}}
    )

    return jsonify({"message": "Comment added successfully"}), 200


# API endpoint to retrieve comments for a book
@app.route('/get-comments', methods=['GET'])
def get_comments():
    book_id = request.args.get('book_id')

    # Inside the get_comments function
    book_id = request.args.get('book_id')
    book = books_collection.find_one({"_id": ObjectId(book_id)})

    print(book)

    if book is None:
        return jsonify({"error": f"Book with ID {book_id} not found", "status_code": 404}), 404

    comments = book.get('comments', [])
    
    # Return only the comments
    return jsonify(comments), 200


# Updated route definition for retrieving average rating
@app.route('/get-average-rating', methods=['GET'])
def get_average_rating():
    book_id = request.args.get('book_id')

    # Inside the get_average_rating function
    book = books_collection.find_one({"_id": ObjectId(book_id)})

    if book is None:
        return jsonify({"error": f"Book with ID {book_id} not found", "status_code": 404}), 404

    ratings = book.get('ratings', [])

    if not ratings:
        return jsonify({"average_rating": 0}), 200

    total_ratings = sum([rating['rating'] for rating in ratings])
    average_rating = total_ratings / len(ratings)

    return jsonify({"average_rating": average_rating}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

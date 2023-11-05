from flask import Flask, jsonify, request, abort
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['geek_text_db']
wishlists_collection = db['whishlists']

#Create the wishlist
@app.route('/create_wishlist', methods=['POST'])
def create_wishlist():
    data = request.json
    user_id = data['user_id']
    wishlist_name = data['wishlist_name']

    #check if there is a wishlist with the same name 
    existing_wishlist = wishlists_collection.find_one({"user_id": user_id, "wishlist_name": wishlist_name})
    if existing_wishlist:
        return jsonify({"message": "Wishlist name already exists for this user."}), 400
    
    wishlist = {
        "user_id": user_id,
        "wishlist_name": wishlist_name,
        "books": []
    }
    wishlists_collection.insert_one(wishlist)

    return jsonify({"message": "Wishlist created successfully."}), 201

#Add a book to a wishlist
@app.route('/add_book_to_wishlist', methods=['POST'])
def add_book_to_wishlist():
    data = request.json()
    book_id = data['bood_id']
    wishlist_id = data['wishlist_id']

    #check if the wishlist exists
    wishlist = wishlists_collection.find_one({"_id": wishlist_id})
    if not wishlist:
        return jsonify({"message": "Wishlist not found."}), 404

    wishlists_collection.update_one({"_id": wishlist_id}, {"$push": {"books": book_id}})

    return jsonify({"message": "Book added to wishlist successfully."}), 200

#Remove a book from a wishlist 
@app.route('/remove_book_from_wishlist', methods=['DELETE'])
def remove_book_from_wishlist():
    data = request.json()
    book_id = data['book_id']
    wishlist_id = data['wishlist_id']

    #check if the wishlist exists
    wishlist = wishlists_collection.find_one({"_id": wishlist_id})
    if not wishlist:
        return jsonify({"message": "Wishlist not found."}), 404

    wishlists_collection.update_one({"_id": wishlist_id}, {"$pull": {"books": book_id}})

    return jsonify({"message": "Book removed from wishlist successfully."}), 200

#Return a list of the books in the wishlist 
@app.route('/list_books_in_wishlist', methods=['GET'])
def list_books_in_wishlist():
    wishlist_id = request.args.get('wishlist_id')

    wishlist = wishlists_collection.find_one({"_id": wishlist_id})
    if not wishlist:
        return jsonify({"message": "Wishlist not found."}), 404

    books_in_wishlist = wishlist['books']
    
    return jsonify({"books_in_wishlist": books_in_wishlist}), 200

if __name__ == '__main__':
    app.run(debug=True)
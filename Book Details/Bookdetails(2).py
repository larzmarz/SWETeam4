from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']

# this fuunction is to check if the ISBN format is valid
def is_valid_isbn(isbn):
    # implementing logic to validate ISBN format here
    # it wilkl return True if valid, False otherwise
    pass

# function will check if author data is valid
def is_valid_author_data(author_data):
    # implementing logic to validate author data here
    # it will return True if valid, False otherwise
    pass

# function to retrieve books that are associated with a specific author from the database
def get_books_by_author(author_id):
    # get books related to the given author_id
    books = list(db.books.find({"author_id": author_id}))
    return books

# this will create a new book
@app.route('/api/books', methods=['POST'])
def create_book_api():
    data = request.get_json()

    # validating ISBN format
    isbn = data.get('isbn')
    if not is_valid_isbn(isbn):
        return jsonify({"error": "Invalid ISBN format"}), 400

    # Now the code will extract book details from the request data
    # then the details will be added to the database for the new book
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    author = data.get('author')
    genre = data.get('genre')
    publisher = data.get('publisher')
    year_published = data.get('year_published')
    copies_sold = data.get('copies_sold')

    # Now, the system is preparing the book data to be inserted into the database
    book = {
        "isbn": isbn,
        "name": name,
        "description": description,
        "price": price,
        "author": author,
        "genre": genre,
        "publisher": publisher,
        "year_published": year_published,
        "copies_sold": copies_sold
    }

    # inserting book into MongoDB collection
    db.books.insert_one(book)
    return jsonify({"message": "Book created successfully"}), 201

# retrieving book details by ISBN
@app.route('/api/books/<string:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    # validating ISBN format
    if not is_valid_isbn(isbn):
        return jsonify({"error": "Invalid ISBN format"}), 400

    # query the database to find the book using the provided ISBN
    book = db.books.find_one({"isbn": isbn})
    if book:
        # returning book details as a JSON response if found
        return jsonify(book), 200
    else:
        # returning error response if the book with the given ISBN is not found
        return jsonify({"error": "Book not found"}), 404

# Endpoint: creating a new author
@app.route('/api/authors', methods=['POST'])
def create_author_api():
    data = request.get_json()

    # validating the author data
    if not is_valid_author_data(data):
        return jsonify({"error": "Invalid author data"}), 400

    # extracting author details from the request data
    # details will be added to the database for the new author
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    biography = data.get('biography')
    publisher = data.get('publisher')

    # preparing author data to be inserted to the database
    author = {
        "first_name": first_name,
        "last_name": last_name,
        "biography": biography,
        "publisher": publisher
    }

    # inserting author into the MongoDB collection
    db.authors.insert_one(author)
    return jsonify({"message": "Author created successfully"}), 201

# retrieving books associated with a specific author by author ID
@app.route('/api/authors/<string:author_id>/books', methods=['GET'])
def get_books_by_author_api(author_id):
    # Gets books associated with the given author ID from the database
    books = get_books_by_author(author_id)
    if books:
        # returning the list of books as a JSON response if found
        return jsonify(books), 200
    else:
        # returning error messsage if no books are found for the given author ID
        return jsonify({"error": "No books found for the given author"}), 404

# Main function: run Flask application
if __name__ == '__main__':
    app.run(debug=True)

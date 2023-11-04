from pymongo import MongoClient

# connection to MongoDB 
client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']

# This function will be used to validate ISBN format. 
def is_valid_isbn(isbn):
    #return true if ISBN is valid or false if otherwise
    return True  

# Function: creates the book
def create_book():
    # accepting user input 
    isbn = input("Enter Book ISBN: ")
    if not is_valid_isbn(isbn):
        print("Invalid ISBN format. Please try again.")
        return

    #all information needed for book detail
    name = input("Enter Book Name: ")
    description = input("Enter Book Description: ")
    price = float(input("Enter Book Price: "))
    author = input("Enter Book Author: ")
    genre = input("Enter Book Genre: ")
    publisher = input("Enter Book Publisher: ")
    year_published = int(input("Enter Year Published: "))
    copies_sold = int(input("Enter Copies Sold: "))

    # preparing book document
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

    # Now it is inserting the book info into the MongoDB collection
    db.books.insert_one(book)
    print("Book created successfully.")

# Main menu
while True:
    print("\nWelcome to Bookstore Management System")
    print("1. Create a Book")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        create_book()
    elif choice == "2":
        print("Thank you for using Bookstore Management System. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

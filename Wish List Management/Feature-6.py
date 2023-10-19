from DatabaseWrapper import Flask, jsonify, request, abort, DESCENDING, DatabaseWrapper

app = Flask(__name__)

db_wrapper = DatabaseWrapper()
# <Collection Name>_collection = db_wrapper.get_collection('<Collection Name>')

# Routes Here

if __name__ == '__main__':
    app.run(debug=True)
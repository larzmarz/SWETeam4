from flask import Flask, request
from flask_mysqldb import MySQL #pip install flask-mysqldb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'geektext'

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/book", methods=['POST'])
def createBook():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        sumary = request.form.get('summary')
        price = request.form.get('price')
        #title = request.json.get('sumary')

        #Creating a connection cursor
        cursor = mysql.connection.cursor()
        query = "INSERT INTO book(title, author, summary, price) VALUES ('"+title+"', '"+author+"', '"+sumary+"', "+price+")"
        cursor.execute(query)
        mysql.connection.commit()
 
        #Closing the cursor
        cursor.close()
       
    return 'book created'
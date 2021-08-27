from flask import Flask
from flask import request
from scraper import connectMongo,getBook,getAuthor
from parser import parser
from bson.json_util import dumps

db_book, db_author = connectMongo()
app = Flask(__name__)

def query(type, query):
	global db_book
	global db_author
	if type ==	"book":
		return db_book.find_one(query,projection= { "_id": 0 })
	elif type == "author":
		return db_author.find_one(query,projection= { "_id": 0 })
	return None

@app.route('/api/books',methods=['GET','POST'])
def booksAPI():
	if request.method == 'GET':
		return dumps(list(db_book.find({}, projection= { "_id": 0 })))
	if request.method == 'POST':
		if not request.is_json:
			return "error", 400
		for d in request.json:
			db_book.insert_one(d)
		return "success", 200

@app.route('/api/authors',methods=['GET','POST'])
def authorsAPI():
	if request.method == 'GET':
		return dumps(list(db_author.find({}, projection= { "_id": 0 })))
	if request.method == 'POST':
		if not request.is_json:
			return "error", 400
		for d in request.json:
			db_author.insert_one(d)
		return "success",200

@app.route('/api/book',methods=['GET','PUT','POST','DELETE'])
def bookapi():
	if request.method == 'GET':
		book_id = request.args.get("id")
		if book_id == None:
			return "book_id empty", 400
		return dumps(db_book.find_one({"book_id" : int(book_id)}, projection= { "_id": 0 }))
	if request.method == 'PUT':
		book_id = request.args.get("id")
		if book_id == None or not request.is_json:
			return "error", 400
		book = dumps(db_book.find_one({"book_id" : int(book_id)}, projection= { "_id": 0 }))
		if type(book) == type(None):
			return "error", 400
		book = db_book.update_one({"book_id" : int(book_id)}, { "$set": request.json})
		return "success",200
	if request.method == 'POST':
		if not request.is_json:
			return "error", 400
		db_book.insert_one(request.json)
		return "success",200
	if request.method == 'DELETE':
		book_id = request.args.get("id")
		if book_id == None:
			return "book_id empty", 400
		book = dumps(db_book.find_one({"book_id" : int(book_id)}, projection= { "_id": 0 }))
		if type(book) == type(None):
			return "error", 400
		db_book.delete_one({"book_id" : int(book_id)})
		return "success",200

@app.route('/api/author',methods=['GET','PUT','POST','DELETE'])
def authorApi():
	if request.method == 'GET':
		book_id = request.args.get("id")
		if book_id == None:
			return "author_id empty", 400
		book = dumps(db_author.find_one({"author_id" : int(book_id)}, projection= { "_id": 0 }))
		print(book)
		if type(book) == type(None):
			return "error", 400
		return book, 200
	if request.method == 'PUT':
		book_id = request.args.get("id")
		if book_id == None	or not request.is_json:
			return "error", 400
		book = dumps(db_author.find_one({"author_id" : int(book_id)}, projection= { "_id": 0 }))
		if type(book) == type(None):
			return "error", 400
		db_author.update_one({"author_id" : int(book_id)}, { "$set": request.json})
		return "success",200
	if request.method == 'POST':
		if not request.is_json:
			return "error", 400
		db_author.insert_one(request.json)
		return "success",200
	if request.method == 'DELETE':
		book_id = request.args.get("id")
		if book_id == None:
			return "author_id empty", 400
		book = dumps(db_author.find_one({"author_id" : int(book_id)}, projection= { "_id": 0 }))
		if type(book) == type(None):
			return "error", 400
		db_author.delete_one({"author_id" : int(book_id)})
		return "success",200

@app.route('/api/search',methods=['GET'])
def getQuery():
	book_id = request.args.get("q")
	if book_id == None:
		return "book_id empty", 400
	type, query = parser(book_id)
	if query == None:
		return "error", 400
	if type == "book":
		return dumps(db_book.find(query, projection= { "_id": 0 }))
	else:
		return dumps(db_author.find(query, projection= { "_id": 0 }))

@app.route('/api/scrape',methods=['POST'])
def scrape():
	url = request.args.get("url")
	if url == None:
		return "error", 400
	if "book" in url:
		getBook(url,db_book)
	elif "author" in url:
		getAuthor(url, db_author)
	return "success", 200

if __name__ == "__main__":
		app.run(debug=True)
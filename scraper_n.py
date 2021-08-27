import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.json_util import dumps
import json
from os import path

author_id = 0
book_id = 0

def connectMongo():
	client = MongoClient("mongodb+srv://morganli:morganli@cluster0.vbvtb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
	db = client.test
	return db["book_b"], db["author_a"]

def getBook(url, db):
	global book_id
	r = requests.get(url)
	soup = BeautifulSoup(r.content, features="html.parser")
	try:
		title = soup.select("#bookTitle")[0].text.strip()
		try:
			ISBN = soup.select("#bookDataBox > div:nth-child(1) > div.infoBoxRowItem")[0].text
			if "ISBN" not in ISBN and not ISBN.isdigit():
				ISBN = soup.select("#bookDataBox > div:nth-child(2) > div.infoBoxRowItem")[0].text
		except Exception:
			ISBN = ""
		author = soup.select("#bookAuthors > span:nth-child(2) > div > a > span")[0].text.strip()
		author_url = soup.select("#bookAuthors > span:nth-child(2) > div > a")[0]["href"].strip()
		rating = soup.select("#bookMeta > span:nth-child(2)")[0].text.strip()
		rating = float(rating)
		rating_count = soup.select("#bookMeta > a:nth-child(7) > meta")[0].text.replace("ratings","").strip()
		rating_count = int(rating_count.replace(",",""))
		review_count = soup.select("#bookMeta > a:nth-child(9)")[0].text.replace("reviews","").strip()
		review_count = int(review_count.replace(",",""))
		image_url = soup.select("#coverImage")[0]["src"]
		similar_books = []
		similar_books_url = set()
		similar_books_element = soup.select("ul")
		# the ul we want is the -4 element in all uls
		if len(similar_books_element) > 26:
			similar_books_element = similar_books_element[22]
		else:
			similar_books_element = similar_books_element[len(similar_books_element)-4]
		# the 1st element is \n then li then \n then li , so we want element index start from 1 and increment by 2
		for i in range(1,len(similar_books_element.contents),2):
			a = similar_books_element.contents[i].contents[1]
			similar_books.append(a.contents[0]["alt"])
			similar_books_url.add(a["href"])
		book = {
			"book_url" : url.replace("http://","").replace("https://",""),
			"title" : title,
			"book_id" : book_id,
			"ISBN" : ISBN,
			"author_url" : author_url.replace("http://","").replace("https://",""),
			"author" : author,
			"rating" : rating,
			"rating_count" : rating_count,
			"review_count" : review_count,
			"image_url" : image_url.replace("http://","").replace("https://",""),
			"similar_books" : similar_books
		}
		db.insert_one(book)
		print("add book "+ title)
		book_id += 1
		return similar_books_url, author_url
	except Exception as e:
		print("add book in "+ url+" fail")
		print(e)
		return [], None

def getAuthor(url, db):
	global author_id
	r = requests.get(url)
	soup = BeautifulSoup(r.content, features="html.parser")
	# error 12
	name = soup.select("body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.reverseColumnSizes > div.rightContainer > div:nth-child(2) > h1 > span")[0].text.strip()
	rating = soup.select("span.rating > span")[0].text.strip()
	rating = float(rating)
	rating_count = soup.select("span.votes > span")[0]["content"]
	rating_count = int(rating_count.replace(",",""))
	review_count = soup.select("span.count > span")[0]["content"]
	review_count = int(review_count.replace(",",""))
	image_url = soup.select("body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.reverseColumnSizes > div.leftContainer.authorLeftContainer")[0].select("img")[0]["src"]
	author_books_tag = soup.select("tr")
	author_books = []
	author_books_url = []
	try:
		for tr_tag in author_books_tag:
			book_name = tr_tag.select("span")[0].text
			book_url = "https://www.goodreads.com/" + tr_tag.select("a")[0]["href"]
			author_books.append(book_name)
			author_books_url.append(book_url)
	except Exception:
		pass
	related_authors = []
	related_authors_url = set()
	r = requests.get(url.replace("show","similar"))
	soup = BeautifulSoup(r.content, features="html.parser")
	author_list = soup.find_all("a", {"class": "gr-h3 gr-h3--serif gr-h3--noMargin"})
	for author in author_list:
		related_authors.append(author.contents[0].text)
		related_authors_url.add(author["href"])
	author = {
		"name" : name,
		"author_url" : url.replace("http://","").replace("https://",""),
		"author_id" : author_id,
		"rating" : rating,
		"rating_count" : rating_count,
		"review_count" : review_count,
		"image_url" : image_url.replace("http://","").replace("https://",""),
		"related_authors" : related_authors,
		"author_books" : author_books
	}
	db.insert_one(author)
	print("add author "+ name)
	author_id += 1
	return related_authors_url

def loop(start_url, db_book, db_author):
	book_urls, author_url = getBook(start_url,db_book)
	t1 = set().union(book_urls)
	t2 = set()
	while len(book_urls) < 200 and len(t1) > 0:
		for url in t1:
			new_urls, _ = getBook(url, db_book)
			book_urls.add(url)
			if len(book_urls) > 10:
				break
			t2.update(new_urls)
		for url in book_urls:
			if url in t2:
				t2.remove(url)
		t1.clear()
		t1.update(t2)
		t2.clear()
	t1.clear()
	t2.clear()
	author_urls = getAuthor(author_url,db_author)
	t1.update(author_urls)
	while len(author_urls) < 50 and len(t1) > 0:
		for url in t1:
			new_urls = getAuthor(url, db_author)
			author_urls.add(url)
			if len(author_urls) > 10:
				break
			t2.update(new_urls)
		for url in author_urls:
			if url in t2:
				t2.remove(url)
		t1.clear()
		t1.update(t2)
		t2.clear()

def load_data(book_file_name, author_file_name, db_book, db_author):
	global book_id
	global author_id
	books = json.load(open(book_file_name))
	for book in books:
		try:
			abook = {
				"book_url" : book["book_url"],
				"title" : book["title"],
				"book_id" : book["book_id"],
				"ISBN" : book["ISBN"],
				"author_url" : book["author_url"],
				"author" : book["author"],
				"rating" : book["rating"],
				"rating_count" : book["rating_count"],
				"review_count" : book["review_count"],
				"image_url" : book["image_url"],
				"similar_books" : book["similar_books"]
			}
			if book["book_id"] < book_id:
				db_book.replace_one({"book_id" :	book["book_id"]}, abook)
			else:
				db_book.insert_one(abook)
		except KeyError:
			print(book)
			print("error loading file")
			return
	authors = json.load(open(author_file_name))
	for author in authors:
		try:
			aauthor = {
				"name" : author["name"],
				"author_url" : author["author_url"],
				"author_id" : author["author_id"],
				"rating" : author["rating"],
				"rating_count" : author["rating_count"],
				"review_count" : author["review_count"],
				"image_url" : author["image_url"],
				"related_authors" : author["related_authors"],
				"author_books" : author["author_books"]
			}
			if author["author_id"] < author_id:
				db_author.replace_one({"author_id" : author["author_id"]}, {
					"$set"
				})
			else:
				db_author.insert_one(aauthor)
		except KeyError:
			print(author)
			print("error loading file")
			return

def export_data(book_file_name, author_file_name, db_book, db_author):
	book_file = open(book_file_name, "w+")
	author_file = open(author_file_name, "w+")
	book_cursor = db_book.find({},projection= { "_id": 0 })
	book_file.write(dumps(list(book_cursor)))
	book_file.close()
	author_file.write(dumps(list(db_author.find({}, projection = { "_id": 0 }))))
	author_file.close()

def test_export_data(book_file_name, author_file_name):
	db_book, db_author = connectMongo()
	if path.exists(book_file_name):
		return False
	export_data(book_file_name, author_file_name, db_book, db_author)
	if not path.exists(book_file_name):
		return False
	books = json.load(open(book_file_name))
	item = db_book.find_one({},{"book_id" : books[0]["book_id"]})
	if books[0]["book_url"] != item["book_url"]:
		return False
	return True

def test_load_data(book_file_name, author_file_name):
	db_book, db_author = connectMongo()
	if not path.exists(book_file_name):
		return False
	load_data(book_file_name, author_file_name, db_book, db_author)
	books = json.load(open(book_file_name))
	item = db_book.find_one({},{"book_id" : books[0]["book_id"]})
	if books[0]["book_url"] != item["book_url"]:
		return False
	return True

def command_line_interface():
	db_book, db_author = connectMongo()
	while True:
		choose = input("enter 1 to start with a url\n enter 2 to add book / author from json\n enter 3 to export book / author\n enter 4 to do rest")
		if choose == "1":
			start_url = input("enter start url: ")
			loop(start_url, db_book, db_author)
		elif choose == "2":
			book_file_name = input("enter book file path: ")
			author_file_name = input("enter author file name: ")
			load_data(book_file_name, author_file_name, db_book, db_author)
		elif choose == "3":
			book_file_name = input("enter book file path: ")
			author_file_name = input("enter author file name: ")
			export_data(book_file_name, author_file_name, db_book, db_author)
		elif choose == "4":
			choose2 = input("enter 1 to get, enter 2 to post, enter 3 to put, enter 4 to delete")
			choose3 = input("enter 1 for book enter 2 for author")
			if choose2 == "1":
				id = input("enter id: ")
				if choose3 == "1":
					r = requests.get("http://localhost:5000/api/book?id="+id)
					print(r.json())
				if choose3 == "2":
					r = requests.get("http://localhost:5000/api/author?id="+id)
					print(r.json())
			if choose2 == "2":
				if choose3 == "1":
					info = eval(input("enter data in dict format:"))
					r =  requests.post("http://localhost:5000/api/book", data=json.dumps(info),  headers={'Content-Type': 'application/json'})
					if r.status_code != 200:
						print("error")
				if choose3 == "2":
					info = eval(input("enter data in dict format:"))
					r =  requests.post("http://localhost:5000/api/author", data=json.dumps(info),  headers={'Content-Type': 'application/json'})
					if r.status_code != 200:
						print("error")
			if choose2 == "3":
				id = input("enter id: ")
				if choose3 == "1":
					info = eval(input("enter data in dict format:"))
					r =  requests.put("http://localhost:5000/api/book?id="+id, data=json.dumps(info),  headers={'Content-Type': 'application/json'})
					if r.status_code != 200:
						print("error")
				if choose3 == "2":
					info = eval(input("enter data in dict format:"))
					r =  requests.put("http://localhost:5000/api/author?id="+id, data=json.dumps(info),  headers={'Content-Type': 'application/json'})
					if r.status_code != 200:
						print("error")
			if choose2 == "4":
				id = input("enter id: ")
				if choose3 == "1":
					r = requests.delete("http://localhost:5000/api/book?id="+id)
					if r.status_code != 200:
						print("error")
				if choose3 == "2":
					r = requests.delete("http://localhost:5000/api/author?id="+id)
					if r.status_code != 200:
						print("error")



command_line_interface()

#getBook("https://www.goodreads.com/book/show/3735293-clean-code?from_search=true&qid=HhMDV0vMa5&rank=1")
#getAuthor("https://www.goodreads.com/author/show/45372.Robert_C_Martin")
#assert test_export_data("book.json","author.json") == True
#assert test_load_data("book.json","author.json") == True
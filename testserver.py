import requests
import json
import unittest
unittest.TestLoader.sortTestMethodsUsing = None
class TestServerMethods(unittest.TestCase):
	def test_get_book(self):
		r = requests.get("http://localhost:5000/api/book?id=2")
		assert r.status_code == 200
		book = r.json()
		assert book["book_id"] == 2

	def test_get_author(self):
		r = requests.get("http://localhost:5000/api/author?id=2")
		assert r.status_code == 200
		book = r.json()
		assert book["author_id"] == 2

	def test_get_search(self):
		r = requests.get("http://localhost:5000/api/search?q=author.author_id:1")
		assert r.status_code == 200
		book = r.json()[0]
		assert book["author_id"] == 1

	def test_post_book(self):
		info = {
			"book_url": "https://www.goodreads.com/book/show/58128.Head_First_Design_Patterns",
			"title": "Head First Design Patterns",
			"book_id": 1998,
			"ISBN": "\n                  0596007124\n                      (ISBN13: 9780596007126)\n",
			"author_url": "https://www.goodreads.com/author/show/32731.Eric_Freeman",
			"author": "Eric Freeman",
			"rating": "4.28",
			"rating_count": "7,400",
			"review_count": "420",
			"image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1408309444l/58128.jpg",
			"similar_books": [
				"Head First 2D Geometry",
				"Head First HTML with CSS & XHTML",
				"Head First Java",
				"Head First JavaScript",
				"Head First Software Development",
				"Head First Web Design",
				"Head First C#",
				"Head First Ajax: A Brain-Friendly Guide",
				"Head First PHP & MySQL",
				"Head First EJB"
			]
		}
		r = requests.post("http://localhost:5000/api/book", data=json.dumps(info),  headers={'Content-Type': 'application/json'})
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/book?id=1998")
		assert r.status_code == 200
		book = r.json()
		assert book["book_id"] == 1998

	def test_post_author(self):
		info = {
				"name": "Robert C. Martin",
				"author_url": "https://www.goodreads.com/author/show/45372.Robert_C_Martin",
				"author_id": 1998,
				"rating": "4.34",
				"rating_count": "29094",
				"review_count": "1915",
				"image_url": "https://images.gr-assets.com/authors/1490470967p5/45372.jpg",
				"related_authors": [
					"Robert C. Martin",
					"Andy Hunt",
					"Steve McConnell",
					"Michael C. Feathers",
					"Kent Beck",
					"Martin Fowler",
					"Eric Freeman",
					"Erich Gamma",
					"Joshua Bloch",
					"Eric Evans",
					"Sam Newman",
					"Steve  Freeman"
				],
				"author_books": [
					"Clean Code: A Handbook of Agile Software Craftsmanship",
					"The Clean Coder: A Code of Conduct for Professional Programmers",
					"Clean Architecture",
					"Agile Software Development, Principles, Patterns, and Practices",
					"Agile Principles, Patterns, and Practices in C#",
					"Clean Agile: Back to Basics",
					"The Robert C. Martin Clean Code Collection",
					"UML for Java Programmers",
					"Pattern Languages of Program Design 3",
					"Design Principles and  Design Patterns"
				]
			}
		r = requests.post("http://localhost:5000/api/author", data=json.dumps(info),  headers={'Content-Type': 'application/json'})
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/author?id=1998")
		assert r.status_code == 200
		book = r.json()
		assert book["author_id"] == 1998

	def test_put_book(self):
		self.test_post_book()
		info = {
			"book_url": "https://www.goodreads.com/book/show/58128.Head_First_Design_Patterns",
			"title": "Head First Design Patterns",
			"book_id": 1998,
			"ISBN": "\n                  0596007124\n                      (ISBN13: 9780596007126)\n",
			"author_url": "https://www.goodreads.com/author/show/32731.Eric_Freeman",
			"author": "Eric Freeman",
			"rating": "5.35",
			"rating_count": "7,400",
			"review_count": "420",
			"image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1408309444l/58128.jpg",
			"similar_books": [
				"Head First 2D Geometry",
				"Head First HTML with CSS & XHTML",
				"Head First Java",
				"Head First JavaScript",
				"Head First Software Development",
				"Head First Web Design",
				"Head First C#",
				"Head First Ajax: A Brain-Friendly Guide",
				"Head First PHP & MySQL",
				"Head First EJB"
			]
		}
		r = requests.put("http://localhost:5000/api/book?id=1998", data=json.dumps(info),  headers={'Content-Type': 'application/json'})
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/book?id=1998")
		assert r.status_code == 200
		book = r.json()
		assert book["rating"] == "5.35"

	def test_put_author(self):
		self.test_post_author()
		info = {
				"name": "Robert C. Martin",
				"author_url": "https://www.goodreads.com/author/show/45372.Robert_C_Martin",
				"author_id": 1998,
				"rating": "5.25",
				"rating_count": "29094",
				"review_count": "1915",
				"image_url": "https://images.gr-assets.com/authors/1490470967p5/45372.jpg",
				"related_authors": [
					"Robert C. Martin",
					"Andy Hunt",
					"Steve McConnell",
					"Michael C. Feathers",
					"Kent Beck",
					"Martin Fowler",
					"Eric Freeman",
					"Erich Gamma",
					"Joshua Bloch",
					"Eric Evans",
					"Sam Newman",
					"Steve  Freeman"
				],
				"author_books": [
					"Clean Code: A Handbook of Agile Software Craftsmanship",
					"The Clean Coder: A Code of Conduct for Professional Programmers",
					"Clean Architecture",
					"Agile Software Development, Principles, Patterns, and Practices",
					"Agile Principles, Patterns, and Practices in C#",
					"Clean Agile: Back to Basics",
					"The Robert C. Martin Clean Code Collection",
					"UML for Java Programmers",
					"Pattern Languages of Program Design 3",
					"Design Principles and  Design Patterns"
				]
			}
		r = requests.put("http://localhost:5000/api/author?id=1998", data=json.dumps(info),  headers={'Content-Type': 'application/json'})
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/author?id=1998")
		assert r.status_code == 200
		book = r.json()
		assert book["rating"] == "5.25"

	def test_delete_book(self):
		r = requests.delete("http://localhost:5000/api/book?id=1998")
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/book?id=1998")
		assert r.status_code == 400

	def test_delete_author(self):
		r = requests.delete("http://localhost:5000/api/author?id=1998")
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/author?id=1998")
		assert r.status_code == 400

	def test_books(self):
		books = [{
			"book_url": "https://www.goodreads.com/book/show/3735293-clean-code?from_search=true&qid=HhMDV0vMa5&rank=1",
			"title": "Clean Code: A Handbook of Agile Software Craftsmanship",
			"book_id": 999,
			"ISBN": "\n                  0132350882\n                      (ISBN13: 9780132350884)\n",
			"author_url": "https://www.goodreads.com/author/show/45372.Robert_C_Martin",
			"author": "Robert C. Martin",
			"rating": "4.40",
			"rating_count": "15,934",
			"review_count": "950",
			"image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1436202607l/3735293._SX318_.jpg",
			"similar_books": [
				"The Pragmatic Programmer: From Journeyman to Master",
				"Design Patterns: Elements of Reusable Object-Oriented Software",
				"Refactoring: Improving the Design of Existing Code",
				"Head First Design Patterns",
				"Code Complete",
				"Effective Java",
				"Test-Driven Development: By Example",
				"Working Effectively with Legacy Code",
				"Domain-Driven Design: Tackling Complexity in the Heart of Software",
				"Designing Data-Intensive Applications",
				"The Software Craftsman: Professionalism, Pragmatism, Pride",
				"The Mythical Man-Month: Essays on Software Engineering",
				"Building Microservices: Designing Fine-Grained Systems",
				"Java Concurrency in Practice",
				"Extreme Programming Explained: Embrace Change (The XP Series)",
				"JavaScript: The Good Parts",
				"Growing Object-Oriented Software, Guided by Tests",
				"Patterns of Enterprise Application Architecture"
			]
		},
		{
			"book_url": "https://www.goodreads.com/book/show/58128.Head_First_Design_Patterns",
			"title": "Head First Design Patterns",
			"book_id": 1000,
			"ISBN": "\n                  0596007124\n                      (ISBN13: 9780596007126)\n",
			"author_url": "https://www.goodreads.com/author/show/32731.Eric_Freeman",
			"author": "Eric Freeman",
			"rating": "4.28",
			"rating_count": "7,400",
			"review_count": "420",
			"image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1408309444l/58128.jpg",
			"similar_books": [
				"Head First 2D Geometry",
				"Head First HTML with CSS & XHTML",
				"Head First Java",
				"Head First JavaScript",
				"Head First Software Development",
				"Head First Web Design",
				"Head First C#",
				"Head First Ajax: A Brain-Friendly Guide",
				"Head First PHP & MySQL",
				"Head First EJB"
			]
		}]
		r = requests.post("http://localhost:5000/api/books", data=json.dumps(books),  headers={'Content-Type': 'application/json'})
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/book?id=999")
		assert r.status_code == 200
		book = r.json()
		assert book["book_id"] == 999


	def test_authors(self):
		books = [ {
				"name": "Harold Abelson",
				"author_url": "www.goodreads.com/author/show/5409448.Harold_Abelson",
				"author_id": 999,
				"rating": 4.45,
				"rating_count": 4400,
				"review_count": 178,
				"image_url": "images.gr-assets.com/authors/1431506374p5/5409448.jpg",
				"related_authors": [
					"Harold Abelson",
					"Andy Hunt",
					"Steve McConnell",
					"Robert Sedgewick",
					"Eric S. Raymond",
					"Paul    Graham",
					"Charles Petzold",
					"Kent Beck",
					"Jon L. Bentley",
					"W. Richard Stevens",
					"Robert C. Martin",
					"Erich Gamma",
					"Joshua Bloch",
					"Thomas H. Cormen",
					"Daniel P. Friedman",
					"Alfred V. Aho",
					"Brian Goetz",
					"Andrew S. Tanenbaum",
					"Eric Evans",
					"Brian W. Kernighan",
					"Randal E. Bryant",
					"Stuart Russell",
					"Douglas Crockford",
					"Miran Lipovača",
					"Douglas R. Hofstadter",
					"Frederick P. Brooks Jr.",
					"Marijn Haverbeke",
					"Martin Kleppmann",
					"Sumita Arora",
					"John Ousterhout"
				],
				"author_books": [
					"Structure and Interpretation of Computer Programs",
					"Turtle Geometry: The Computer as a Medium for Exploring Mathematics",
					"The Improvement of Intelligence Testing",
					"Apple Logo",
					"Ti LOGO",
					"Revised [5] Report on the Algorithmic Language Scheme",
					"LOGO for the Macintosh: An Introduction Through Object LOGO",
					"Calculus of Elementary Functions",
					"Structure and Interpretation of Computer Programs",
					"Instructor's Manual to Accompany Structure and Interpretation of Computer Programs"
				]
			},
			{
				"name": "Kevin Werbach",
				"author_url": "www.goodreads.com/author/show/6535101.Kevin_Werbach",
				"author_id": 1999,
				"rating": 3.74,
				"rating_count": 1065,
				"review_count": 108,
				"image_url": "s.gr-assets.com/assets/nophoto/user/m_200x266-d279b33f8eec0f27b7272477f09806be.png",
				"related_authors": [
					"Kevin Werbach",
					"Gary Chapman",
					"Ram Charan",
					"Robert A. Johnson",
					"Debbie Macomber",
					"Paul Ekman",
					"Tess Gerritsen",
					"Rosamunde Pilcher",
					"Geoffrey A. Moore",
					"Brandon Sanderson",
					"Marc Benioff",
					"Anders Hansen",
					"Amy C. Edmondson",
					"Bruce Judson",
					"Eric Ries",
					"Emma Cline",
					"Jane McGonigal",
					"Bernadette Jiwa",
					"Brian  Burke",
					"Bradley R. Staats",
					"George Berkowski",
					"Laszlo Bock",
					"Yu-kai Chou",
					"Satya Nadella",
					"C.F. Iggulden",
					"Дмитрий Троцкий",
					"Lina Vėželienė"
				],
				"author_books": [
					"For the Win",
					"The Gamification Toolkit",
					"The Blockchain and the New Architecture of Trust",
					"Pergalės technika: kaip žaidybinis mąstymas gali pakeisti jūsų organizaciją",
					"For the Win, Revised and Updated Edition: The Power of Gamification and Game Thinking in Business, Education, Government, and Social Impact",
					"Network Challenge (Chapter 24): The: Telecommunications: Network Strategies for Network Industries?",
					"After the Digital Tornado: Networks, Algorithms, Humanity"
				]
			}]
		r = requests.post("http://localhost:5000/api/authors", data=json.dumps(books),  headers={'Content-Type': 'application/json'})
		assert r.status_code == 200
		r = requests.get("http://localhost:5000/api/author?id=1999")
		assert r.status_code == 200
		book = r.json()
		assert book["author_id"] == 1999

if __name__ == '__main__':
    unittest.main()
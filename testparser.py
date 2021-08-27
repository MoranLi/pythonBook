from parser import * 

import unittest
class testParser(unittest.TestCase):
	def test_valid_attribute(self):
		assert validAttribute("book","book_id") == True
		assert validAttribute("book","id") == False
		assert validAttribute("author","author_id") == True
		assert validAttribute("author","id") == False
		assert validAttribute("temp","temp") == False

	def test_valid_type(self):
		assert validType("book") == True
		assert validType("hh") == False

	def test_valid_value(self):
		assert validValue("\"hello.py") == False
		assert validValue("\"hellow.py\"") == True
		assert validValue("") == False
		assert validValue("NOT ") == False
		assert validValue("NOT 123") == True

	def test_valid_condition(self):
		assert validCondition([["book","book_id"],["123"]]) == True
		assert validCondition([["book","id"],["123"]]) == False

	def test_split_condition(self):
		ans = splitCondition("book.book_id:123")
		assert ans[0][0] == "book"
		assert ans[0][1] == "book_id"
		assert ans[1] == "123"

	def test_parser(self):
		type, ans = parser("book.book_id:12 AND book.rating_count:1")
		assert type == "book"
		assert "$and" in ans
		assert len(ans["$and"]) == 2

if __name__ == '__main__':
    unittest.main()
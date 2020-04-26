from application import *
from models import *

def test_bookreads_api():
	book = Book.query.get("1416949658")
	# response = bookreads_api("1416949658")
	# print(response)
	print(book.title)

test_bookreads_api()
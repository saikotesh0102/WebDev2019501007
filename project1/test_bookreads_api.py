import os,unittest
from models import Book,app,db
from flask import session

class TestCase(unittest.TestCase):
    def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False

		if not os.getenv("DATABASE_URL"):
			raise RuntimeError("DATABASE_URL is not set")
		self.app = app.test_client()
		self.assertEqual(app.DEBUG, False)
		db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_bookreads_api(self):
        book = Book(isbn = "123456", name = "2States", author = "Chetan Bhagat", publicationyear = "2015")
        db.session.add(book)
        db.session.commit()
        name = Book.query.get('123456').name
        assert name == '2States'
        book = Book(isbn = "123457", name = "Revolution2020", author = "Chetan Bhagat", publicationyear = "2013")
        db.session.add(book)
        db.session.commit()
        name = Book.query.get('Chetan Bhagat').name
        assert name == ['2States','Revolution2020']

if __name__ == '__main__':
    unittest.main()
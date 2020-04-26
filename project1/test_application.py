# project1/test_basic.py

import os,unittest
from flask_sqlalchemy import sqlalchemy
from models import *
from application import *

class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        # Check for environment variable
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
    ########################
    #### helper methods ####
    ########################
     
    def register(self, email, password):
        return self.app.post('/register',data=dict(email=email, psw=password),follow_redirects=True)
     
    def login(self, email, password):
        return self.app.post('/auth',data=dict(email=email, psw=password),follow_redirects=True)
     
    def logout(self):
        return self.app.get('/logout',follow_redirects=True)

    def get_book(self, type1):
        return self.app.get('/books', data=dict(isbn=type1),follow_redirects=True)
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_admin(self):
        response = self.app.get("/admin")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_login_invalid(self):
    #     response = self.login('adminmsitprogram.net', 'a1dmin')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Please enter valid email', response.data)

    # def test_invalid_user_register(self):
    #     response = self.register('admin@msitprogram.net', 'a1dmin')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Email already registered please login', response.data)

    # def test_valid_user_login(self):
    #     response = self.login('admin@msitprogram.net', 'admin')
    #     self.assertEqual(response.status_code, 200)

    # def test_invalid_user_login(self):
    #     response = self.login('admin@msitprogram.net', 'a1dmin')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'wrong password', response.data)

if __name__ == "__main__":
    unittest.main()
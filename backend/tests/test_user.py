#!/usr/bin/python3

import unittest
from models.user import User
from utils.database import users_collection
from pymongo import MongoClient
import bcrypt


class TestUserModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient('localhost', 27017)
        cls.test_db = cls.client["test_database"]
        cls.users_collection = cls.test_db["users"]
        user_collection = cls.users_collection

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database("test_database")
        cls.client.close()

    def setUp(self):
        users_collection.delete_many({})

    def test_register_user(self):
        email = "test@example.com"
        password = "password123"
        user = User.register(email, password)
        print("Registered user:", user)
        found_user = users_collection.find_one({"email": email})
        print("Found user:", found_user)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user["email"], email)
        self.assertTrue(User.verify_password(password, found_user["password"].encode('utf-8')))

    def test_find_by_email(self):
        email = "findme@example.com"
        password = "mypassword"
        User.register(email, password)
        user = User.find_by_email(email)
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], email)

    def test_verify_password(self):
        password = "securepassword"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.assertTrue(User.verify_password(password, hashed_password.encode('utf-8')))
        self.assertFalse(User.verify_password("wrongpassword", hashed_password.encode('utf-8')))

    def test_delete_by_email(self):
        email = "delete@example.com"
        password = "password"
        User.register(email, password)
        User.delete_by_email(email)
        user = User.find_by_email(email)
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()

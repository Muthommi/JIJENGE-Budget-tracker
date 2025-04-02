#!/usr/bin/python3

import bcrypt
from bson import ObjectId
from utils.database import users_collection


class User:
    collection = users_collection

    @staticmethod
    def register(email, password):
        hashed_password = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
        )

        user = {
            "email": email,
            "password": hashed_password.decode('utf-8')
        }

        users_collection.insert_one(user)
        return user

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def verify_password(password, hashed_password):
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    @staticmethod
    def delete_by_email(email):
        return users_collection.delete_one({"email": email})

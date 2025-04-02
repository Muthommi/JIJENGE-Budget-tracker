#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['finance_tracker']

users_collection = db['users']
transactions_collection = db['transactions']

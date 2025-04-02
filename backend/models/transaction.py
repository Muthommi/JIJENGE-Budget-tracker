#!/usr/bin/python3

from utils.database import transactions_collection
from bson import ObjectId
from datetime import datetime


class Transaction:
    @staticmethod
    def create(data):
        if isinstance(data.get('date'), str):
            data['date'] = datetime.strptime(data['date'], '%a, %d %b %Y %H:%M:%S %Z')
        transaction_id = transactions_collection.insert_one(data).inserted_id
        inserted_transaction = transactions_collection.find_one({"_id": transaction_id})
        print(f"Inserted Transaction: {inserted_transaction}")
        return inserted_transaction

    @staticmethod
    def add_transaction(user_id, amount, category, description):
        transaction = {
                "user_id": user_id,
                "amount": amount,
                "category": category,
                "description": description,
                "date": datetime.utcnow()
        }
        transactions_collection.insert_one(transaction)
        return transaction

    @staticmethod
    def get_transactions_by_user(user_id):
        return list(transactions_collection.find({"user_id": user_id}))

    @staticmethod
    def get_monthly_summary(user_id, month, year):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        print(f"Start Date: {start_date}, End Date: {end_date}")
        pipeline = [
            {"$match": {"user_id": user_id, "date": {"$gte": start_date, "$lt": end_date}}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
        ]
        print(f"Pipeline: {pipeline}")
        summary = list(transactions_collection.aggregate(pipeline))
        return summary

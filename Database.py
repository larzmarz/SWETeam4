from decouple import config
from pymongo import MongoClient, DESCENDING
from flask import Flask, jsonify, request, abort

class DatabaseWrapper:
    def __init__(self):
        MONGODB_URI = config('MONGODB_URI')
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['geek_text_db']

    def get_collection(self, collection_name):
        return self.db[collection_name]

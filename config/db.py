from pymongo import MongoClient
from config.keys import MongoCli

conn = MongoClient(MongoCli)
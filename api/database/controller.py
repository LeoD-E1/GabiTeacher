from flask import Flask
from flask_pymongo import PyMongo

from api.commons.env import env

app = Flask(__name__)
#app.config["MONGO_URI"] = env.get("MONGODB_URI") + "?retryWrites=false"
app.config["MONGO_URI"] = env.get("MONGODB_URI_LOCAL")
mongo = PyMongo(app)


def find(model, condition):
    return mongo.db[model].find(condition)


def find_one(model, condition):
    return mongo.db[model].find_one(condition)


def insert(model, condition):
    return mongo.db[model].insert_one(condition)

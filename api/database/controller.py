from flask import Flask
from flask_pymongo import PyMongo

from api.commons.env import env

app = Flask(__name__)
app.config["MONGO_URI"] = env.get('MONGODB_URI') + '?retryWrites=false'
mongo = PyMongo(app)


def find(model):
    return mongo.db[model].find()

def find_one(model):
    return mongo.db[model].find_one()

def insert(model, reg):
    return mongo.db[model].insert_one({'name': 'Mycol'})


import hashlib
import json

from bson.objectid import ObjectId
from flask import Blueprint, request

from config import db
from src.models.userModel import User

userCtrl = Blueprint('user', __name__)


@userCtrl.route('/create', methods=['POST'])
def create_user():
    data = request.json
    password = hashlib.sha256(data["password"].encode(
        'utf-8')).hexdigest()
    user = User(data["name"], password, data["email"], data["role"])

    result = db.users.insert_one(user.__dict__)
    return json.dumps({'userId': result.inserted_id}, default=str)


@userCtrl.route('/update', methods=['PUT'])
def update_user():
    data = request.json
    password = hashlib.sha256(data["password"].encode(
        'utf-8')).hexdigest()
    result = db.users.update_one({'_id': ObjectId(data["id"])}, {
        '$set': {'username': data["name"],'email': data["email"],'password': password}})
    return json.dumps({'acknowledged': result.acknowledged}, default=str)


@userCtrl.route('/', methods=['GET'])
def find_all():
    cursor = db.users.find({'role':'employee'})
    result = [document for document in cursor]
    return json.dumps(result, default=str)


@userCtrl.route('/find', methods=['GET'])
def find_one():
    data = request.args.get('user')
    result = db.users.find_one({'_id': ObjectId(data)})
    return json.dumps(result, default=str)

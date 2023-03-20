import hashlib
import json

from flask import Blueprint, request

from config import db

authCtrl = Blueprint('auth', __name__)


@authCtrl.route('/login', methods=['POST'])
def login():
    data = request.json

    password = hashlib.sha256(data["password"].encode(
        'utf-8')).hexdigest()

    result = db.users.find_one(
        {'username': data['username'], 'password': password})

    return json.dumps(result, default=str)

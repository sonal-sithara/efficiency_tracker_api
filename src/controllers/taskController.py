import json
import os
from datetime import datetime

from bson.objectid import ObjectId
from flask import Blueprint, request

from config import db
from src.models.taskModel import Task
from src.controllers.userController import find_all

taskCtrl = Blueprint('task', __name__)


@taskCtrl.route('/create', methods=['POST'])
def create_task():
    form = request.form
    data = json.loads(form['data'])

    if 'attachment' in request.files:
        file = request.files['attachment']

        filename = file.filename
        file.save(os.path.join(os.environ['UPLOAD_FOLDER'], filename))

    task = Task(data["id"], data["name"], data["desc"],
                data["submissionDate"], filename)

    result = db.tasks.insert_one(task.__dict__)

    return json.dumps({'taskId': result.inserted_id}, default=str)


@taskCtrl.route('/start', methods=['POST'])
def start_task():
    data = request.json

    result = db.tasks.update_one({'_id': ObjectId(data['id'])}, {
        '$set': {'startTime': data['startTime'], 'lastStartTime': data['startTime'], 'isTaskStart': True}})

    return json.dumps({'acknowledged': result.acknowledged}, default=str)


@taskCtrl.route('/start_pause', methods=['POST'])
def start_pause_task():
    data = request.json

    result = db.tasks.update_one({'_id': ObjectId(data['id'])}, {
        '$set': {'lastStartTime': data['startTime'], 'isPause': False}})

    return json.dumps({'acknowledged': result.acknowledged}, default=str)


@taskCtrl.route('/pause', methods=['POST'])
def pause_task():
    data = request.json

    doc = db.tasks.find_one({'_id': ObjectId(data["id"])})

    startTime = datetime.strptime(doc['lastStartTime'], "%Y-%m-%d %H:%M:%S")
    pauseTime = datetime.strptime(data['pauseTime'], "%Y-%m-%d %H:%M:%S")

    time_diff = ((pauseTime - startTime).total_seconds() / 60.0) + \
        doc['spendTime']

    result = db.tasks.update_one({'_id': ObjectId(data['id'])}, {
        '$set': {'spendTime': time_diff, 'isPause': True}})

    return json.dumps({'acknowledged': result.acknowledged}, default=str)


@taskCtrl.route('/end', methods=['POST'])
def end_task():
    data = request.json

    doc = db.tasks.find_one({'_id': ObjectId(data["id"])})

    startTime = datetime.strptime(doc['lastStartTime'], "%Y-%m-%d %H:%M:%S")
    endTime = datetime.strptime(data['endTime'], "%Y-%m-%d %H:%M:%S")

    time_diff = ((endTime - startTime).total_seconds() / 60.0) + \
        doc['spendTime']

    result = db.tasks.update_one({'_id': ObjectId(data['id'])}, {
        '$set': {'spendTime': time_diff, 'isPause': True, 'isTaskComplete': True}})

    return json.dumps({'acknowledged': result.acknowledged}, default=str)


@taskCtrl.route('/', methods=['GET'])
def find_all():
    cursor = db.tasks.find()
    result = [document for document in cursor]
    return json.dumps(result, default=str)


@taskCtrl.route('/find_by_user', methods=['GET'])
def find_by_user():
    data = request.json

    cursor = db.tasks.find({'userId': data['userId']})
    result = [document for document in cursor]
    return json.dumps(result, default=str)

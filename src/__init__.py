from flask import Flask
from flask_cors import CORS

from src.controllers.taskController import taskCtrl
from src.controllers.userController import userCtrl
from src.controllers.authController import authCtrl
from src.ml_modal.modalController import mlCtrl


app = Flask(__name__)
cors = CORS(app)


app.register_blueprint(userCtrl, url_prefix='/user')
app.register_blueprint(taskCtrl, url_prefix='/task')
app.register_blueprint(authCtrl, url_prefix='/auth')
app.register_blueprint(mlCtrl, url_prefix='/ml')

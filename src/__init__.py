from flask import Flask

from src.controllers.taskController import taskCtrl
from src.controllers.userController import userCtrl
from src.controllers.authController import authCtrl


app = Flask(__name__)

app.register_blueprint(userCtrl, url_prefix='/user')
app.register_blueprint(taskCtrl, url_prefix='/task')
app.register_blueprint(authCtrl, url_prefix='/auth')

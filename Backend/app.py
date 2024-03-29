from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from routes.exercise import app_exercise
from routes.login import app_login
from routes.routine import app_routine
from routes.register import app_register
from routes.diet import app_diet
from routes.trainer import app_trainer
from routes.client import app_client
from routes.analytics import app_analytics

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)

app = Flask(__name__)
CORS(app)
api = Api(app)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(app_exercise)
app.register_blueprint(app_routine)
app.register_blueprint(app_login)
app.register_blueprint(app_register)
app.register_blueprint(app_diet)
app.register_blueprint(app_trainer)
app.register_blueprint(app_client)
app.register_blueprint(app_analytics)
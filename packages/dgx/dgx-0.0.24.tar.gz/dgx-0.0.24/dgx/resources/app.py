# manejo de cola (NO ORDENAR)
import eventlet
eventlet.monkey_patch()

# dependencias
from flask import Flask, jsonify, request, make_response
from flask_json_pattern import ValidationError
from mongoCon import MongoCon
from flask_socketio import SocketIO
from const import ENV, MONGO_CONN
from utils.helpers import CustomJSONEncoder
from datetime import datetime
from werkzeug import exceptions
import traceback
import json


# instancia de aplicacion con socket
app = Flask(__name__)
app.secret_key = "@3!f3719em$893&"
app.json_encoder = CustomJSONEncoder
json.JSONEncoder = CustomJSONEncoder
socketio = SocketIO(app, cors_allowed_origins="*", message_queue='redis://', async_mode='eventlet')


# saludo
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to <<API_NAME>> API", "ENV": ENV, "db": MONGO_CONN['database']})


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        return make_response(jsonify({'msg': error.description.message}), 400)
    return make_response(jsonify({'msg': str(error)}), 400)


@app.errorhandler(Exception)
def handle_exception(e):
    traceback.print_exc()
    if isinstance(e, exceptions.HTTPException):
        return make_response(jsonify({'msg': e.name}), e.code)
    return make_response(jsonify({'msg': str(e)}), 500)


@app.before_request
def before_request_func():
    with MongoCon() as cnx:
        cnx.request_log.insert({
            "datetime": datetime.now(),
            "headers": dict(request.headers),
            "method": request.method,
            "endpoint": request.path,
            "body": request.json,
            "remote_addr": request.remote_addr,
            "browser": request.user_agent.browser,
            "language": request.user_agent.language,
            "platform": request.user_agent.platform
        })

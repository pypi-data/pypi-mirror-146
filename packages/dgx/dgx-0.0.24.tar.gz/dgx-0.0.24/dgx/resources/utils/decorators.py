from flask import jsonify, make_response, request, session
from dgapi import DGAPI
from functools import wraps
from logging import error
import jwt


def is_authorize():
    return DGAPI.get('valid_token').status_code == 200


def login_required(f):
    """Full login"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('security-token')
        try:
            data = jwt.decode(token, '@3!f3719em$893&')  # token decode
        except Exception:   # jwt.ExpiredSignatureError
            error('TOKEN NO VALID')
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
        else:  # token valido
            session['user_id'] = data['user_id']
            session['user_application_id'] = data['user_application_id']
            session['user_name'] = data['name']
            session['user_email'] = data.get('email', '')
            session['roles'] = data.get('security_actions', [])
            if is_authorize():
                return f(*args, **kwargs)
            else:
                return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    return decorated


def login_script(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token', '')
        session['token'] = token
        if token == '5gABTw3tXCS{]NN[fk,dUWKcmr3,DaHoa[hiSTfVzq.cZp;W72B[CU.7,kqA(}':
            return f(*args, **kwargs)
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    return decorated

from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_json_pattern import json_pattern
from utils.decorators import login_required
from dgapi import DGAPI


psnl = Blueprint('personnel', __name__)


@psnl.route('/search', methods=['POST'])
@login_required
@json_pattern({
    'search': {'type': str},
})
@swag_from('./docs/search.yml')
def search():
    resp = DGAPI.post('get_personnel', request.json)
    return jsonify(resp.json())


@psnl.route('/get_by_id', methods=['POST'])
@login_required
@json_pattern({
    'id': {'type': int},
})
@swag_from('./docs/get_by_id.yml')
def get_by_id():
    resp = DGAPI.get('get_user_by_id/%s' % request.json.get("id"))
    if resp.status_code == 200:
        item = resp.json()
        del item['apps']
        return jsonify(item)
    return jsonify(None)


@psnl.route('/update', methods=['POST'])
@login_required
@json_pattern({
    'id': {'type': int},
})
@swag_from('./docs/update.yml')
def update():
    request.json.pop('apps', None)
    resp = DGAPI.post('update_user', request.json)
    return jsonify(resp.json())


@psnl.route('/get_roles', methods=['GET'])
@login_required
@swag_from('./docs/get_roles.yml')
def get_roles():
    resp = DGAPI.get('get_roles')
    return jsonify(resp.json())

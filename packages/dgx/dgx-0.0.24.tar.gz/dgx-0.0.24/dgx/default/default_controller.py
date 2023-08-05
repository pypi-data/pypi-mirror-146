from flask import Blueprint, jsonify
from flasgger import swag_from
from flask_json_pattern import json_pattern
from utils.decorators import login_required


default = Blueprint('default', __name__)


@default.route('/search', methods=['POST'])
@login_required
@json_pattern({
    'search': {'type': str},
})
@swag_from('./docs/search.yml')
def search():
    return jsonify([])

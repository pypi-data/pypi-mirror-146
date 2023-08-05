from flask import Blueprint, request, jsonify, session
from flasgger import swag_from
from flask_json_pattern import json_pattern
from utils.decorators import login_required
from dgapi import DGAPI


brand = Blueprint('brand', __name__)


@brand.route('/get_all', methods=['GET'])
@login_required
@swag_from('./docs/get_all.yml')
def get_all():
    resp = DGAPI.get('get_all_brands')
    return jsonify(resp.json())


@brand.route('/get_by_dealer', methods=['GET'])
@login_required
@swag_from('./docs/get_by_dealer.yml')
def get_by_dealer():
    resp = DGAPI.post('get_brands_by_dealer', {"dealer_code": session['dealer']}, {"Content-Type": "application/json"})
    return jsonify(resp.json())


@brand.route('/search', methods=['POST'])
@login_required
@json_pattern({
    'search': {'type': str},
})
@swag_from('./docs/search.yml')
def search():
    resp = DGAPI.post('find_brand', request.json)
    return jsonify(resp.json())

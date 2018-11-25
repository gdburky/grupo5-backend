from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests


API_PATH = 'http://charette9.ing.puc.cl/api'

class Post(Resource):
    API_PATH_P = API_PATH + '{}'.format('/topics')

    def get(self):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_P, headers={'Authorization': 'Bearer ' + token})
        return jsonify(resp.json())
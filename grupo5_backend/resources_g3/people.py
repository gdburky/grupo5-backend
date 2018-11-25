from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests


API_PATH = 'http://charette9.ing.puc.cl/api'

class PersonRegister(Resource):
    API_PATH_PR = API_PATH + '{}'.format('/users')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help= 'No email provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help= 'No password provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'username',
            required=True,
            help= 'No username provided',
            location=['form', 'json',]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_PR, data=args)
        return jsonify(resp.json())


    def get(self):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PR, headers={'Authorization': 'Bearer ' + token})
        return jsonify(resp.json())


class PersonLogin(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/login')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help= 'No email provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help= 'No password provided',
            location=['form', 'json', ]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_PL, data=args)
        data = {'id': resp.json()['token']}
        resp2 = requests.get('http://charette9.ing.puc.cl/api/user', headers={'Authorization': 'Bearer ' + data['token']})
        data['userId'] = resp2.json()['_id']
        return jsonify(data)

g3_person_api = Blueprint('resources_g3.people', __name__)

api = Api(g3_person_api)
api.add_resource(PersonRegister, '/people')
api.add_resource(PersonLogin, '/people/login')




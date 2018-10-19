from flask import Blueprint, abort
from flask_restful import Resource, Api, reqparse

import requests

API_PATH = 'charette15.ing.puc.cl/api'

class PersonRegister(Resource):
    API_PATH_PR = API_PATH + '{}'.format('/people')

    def post(self):
        args = reqparse.RequestParser().parse_args()
        resp = requests.post(self.API_PATH_PR, data=args)
        if resp.status_code == 200:
            return resp.text
        else: 
            abort(resp.status_code)


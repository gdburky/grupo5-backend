from flask import Blueprint, abort
from flask_restful import Resource, Api

import requests

API_PATH = 'charette15.ing.puc.cl/api'


class ResponseCollection(Resource):
    API_PATH_RC = API_PATH + '{}'.format('/responses')

    def get(self):
        resp = requests.get(self.API_PATH_RC)
        if resp.status_code == 200:
            return resp.text
        else: 
            abort(resp.status_code)

class Response(Resource):
    API_PATH_R = API_PATH + '{}'.format('/responses/{}')

    def get(self, id_):
        resp = requests.get(self.API_PATH_R.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


responses_api = Blueprint('resources.responses', __name__)

api = Api(responses_api)
api.add_resource(ResponseCollection, '/responses')

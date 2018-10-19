from flask import Blueprint, abort
from flask_restful import Resource, Api

import requests

API_PATH = 'charette15.ing.puc.cl/api'


class SubscriptionCollection(Resource):
    API_PATH_SC = API_PATH + '{}'.format('/subscriptions')

    def get(self):
        resp = requests.get(self.API_PATH_SC)
        if resp.status_code == 200:
            return resp.text
        else: 
            abort(resp.status_code)


subscriptions_api = Blueprint('resources.subscriptions', __name__)

api = Api(subscriptions_api)
api.add_resource(SubscriptionCollection, '/subscriptions')

from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api

import requests

API_PATH = 'http://.charette15.ing.puc.cl/api'


class SubscriptionCollection(Resource):
    API_PATH_SC = API_PATH + '{}'.format('/subscriptions')

    def get(self):
        resp = requests.get(self.API_PATH_SC)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else: 
            abort(resp.status_code)
    
    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_SC, data=args)
        if resp.status_code == 201:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class Subscription(Resource):
    API_PATH_S = API_PATH + '{}'.format('/subscriptions/{}')

    def get(self, id_):
        resp = requests.get(self.API_PATH_S.format(id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)
    def delete(self, id_):
        resp = requests.delete(self.API_PATH_S.format(id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


subscriptions_api = Blueprint('resources.subscriptions', __name__)

api = Api(subscriptions_api)
api.add_resource(SubscriptionCollection, '/subscriptions')
api.add_resource(Subscription, '/subscriptions/<int:id_>')
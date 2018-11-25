from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

API_PATH = 'http://.charette15.ing.puc.cl/api'


class SubscriptionCollection(Resource):
    API_PATH_SC = API_PATH + '{}'.format('/people/{}/subscriptions')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'notification',
            required=True,
            help= 'No notification provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'personId',
            required=True,
            help= 'No personId provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'postId',
            required=True,
            help= 'No postId provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self, id_):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_SC.format(id_), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        token = request.args.get('access_token','')
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_SC.format(id_), data=args, params={'access_token': token})
        if resp.status_code == 201:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class Subscription(Resource):
    API_PATH_S = API_PATH + '{}'.format('/people/{}/subscriptions/{}')

    def get(self,personId, id_):
        resp = requests.get(self.API_PATH_S.format(personId,id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)
    def delete(self,personId, id_):
        token = request.args.get('access_token','')
        resp = requests.delete(self.API_PATH_S.format(personId,id_),params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


subscriptions_api = Blueprint('resources.subscriptions', __name__)

api = Api(subscriptions_api)
#api.add_resource(SubscriptionCollection, 'people/<int:id_>/subscriptions')
#api.add_resource(Subscription, 'people/<int:personId>/subscriptions/<int:id_>')

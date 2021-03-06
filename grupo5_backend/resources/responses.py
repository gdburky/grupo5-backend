from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

# from resources.service import serviceId

API_PATH = 'http://charette15.ing.puc.cl/api'


class ResponseCollection(Resource):
    API_PATH_RC = API_PATH + '{}'.format('/responses')

    def get(self):
        resp = requests.get(self.API_PATH_RC)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class Response(Resource):
    API_PATH_R = API_PATH + '{}'.format('/services/{}/posts/{}/messages/{}/responses/{}')

    def get(self, postId, msgId, id_):
        global serviceId
        resp = requests.get(self.API_PATH_R.format(serviceId, postId, msgId, id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def delete(self, id_):
        resp = requests.delete(self.API_PATH_R.format(id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class ResponseCollectionCreate(Resource):
    API_PATH_R_CREATE = API_PATH + '{}'.format('/messages/{}/responses')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'description',
            required=True,
            help= 'No description provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self, msgId):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_R_CREATE.format(msgId), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, msgId):
        global serviceId
        args = self.reqparse.parse_args()
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_R_CREATE.format(msgId), data=args, params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


responses_api = Blueprint('resources.responses', __name__)

api = Api(responses_api)
#api.add_resource(ResponseCollection, '/responses')
#api.add_resource(Response, '/posts/<int:postId>/messages/<int:msgId>/responses/<int:id_>')
#api.add_resource(ResponseCollectionCreate, '/messages/<int:msgId>/responses')

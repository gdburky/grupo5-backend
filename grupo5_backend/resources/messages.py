from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

SERVICEID = '181'
API_PATH = 'http://charette15.ing.puc.cl/api'

'''
class MessagesCollection(Resource):
    API_PATH_MC = API_PATH + '{}'.format('/messages')

    def get(self):
        args = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_MC, params={'access_token': args})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)
'''

class Message(Resource):
    API_PATH_M = API_PATH + '{}'.format('/messages/{}')

    def get(self, id_):
        args = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_M.format(id_), params={'access_token': args})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def delete(self, id_):
        args = request.args.get('access_token','')
        resp = requests.delete(self.API_PATH_M.format( id_), params={'access_token': args})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

'''
class MessageCreate(Resource):
    API_PATH_M_CREATE = API_PATH + '{}'.format('/posts/{}/messages')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'description',
            required=True,
            help= 'No description provided',
            location=['form', 'json',]
        )
        super().__init__()

    def post(self, postId):
        args = self.reqparse.parse_args()
        params = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_M_CREATE.format(postId), data=args, params={'access_token': params})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)
'''

class MessagesResponsesCollection(Resource):
    API_PATH_MRC = API_PATH + '{}'.format('/messages/{}/responses')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'description',
            required=True,
            help= 'No description provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self, id_):
        params = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_MRC.format(id_), params={'access_token': params})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = self.reqparse.parse_args()
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_MRC.format(id_), data=args, params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class MessagesFilter(Resource):
    API_PATH_MHC = API_PATH + '{}'.format('/services/{}/filterMessages/{}')

    def get(self, string_):
        params = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_MHC.format(SERVICEID, string_), params={'access_token': params})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


messages_api = Blueprint('resources.messages', __name__)

api = Api(messages_api)
#api.add_resource(MessagesCollection, '/messages')
api.add_resource(MessagesFilter, '/messages/filter/<string:string_>')
api.add_resource(Message, '/messages/<int:id_>')
#api.add_resource(MessageCreate, '/posts/<int:postId>/messages', endpoint='messagecreate')
api.add_resource(MessagesResponsesCollection, '/messages/<int:id_>/responses')
#api.add_resource(MessagesHashtagCollection, '/filterMessages/filterString')

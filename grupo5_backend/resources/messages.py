from flask import Blueprint, abort, request
from flask_restful import Resource, Api

import requests

API_PATH = 'charette15.ing.puc.cl/api'


class MessagesCollection(Resource):
    API_PATH_MC = API_PATH + '{}'.format('/messages')

    def get(self):
        resp = requests.get(self.API_PATH_MC)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class Message(Resource):
    API_PATH_M = API_PATH + '{}'.format('/messages/{}')

    def get(self, id_):
        resp = requests.get(self.API_PATH_M.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)
    def delete(self, id_):
        resp = requests.delete(self.API_PATH_M.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


class MessagesResponsesCollection(Resource):
    API_PATH_MRC = API_PATH + '{}'.format('/messages/{}/responses')

    def get(self, id_):
        resp = requests.get(self.API_PATH_MRC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_MRC.format(id_), data=args)
        if resp.status_code == 201:
            return resp.text
        else:
            abort(resp.status_code)


class MessagesHashtagCollection(Resource):
    API_PATH_MHC = API_PATH + '{}'.format('messages/filter/{}')

    def get(self, hashtag):
        resp = requests.get(self.API_PATH_MHC.format(hashtag))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


messages_api = Blueprint('resources.messages', __name__)

api = Api(messages_api)
api.add_resource(MessagesCollection, '/messages')
api.add_resource(Message, '/messages/<int:id_>')
api.add_resource(MessagesResponsesCollection, '/messages/<int:id_>/responses')
api.add_resource(MessagesHashtagCollection, '/messages/filter/<string:hashtag>')

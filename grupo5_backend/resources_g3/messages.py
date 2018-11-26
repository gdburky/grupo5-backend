from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

SERVICEID = '175'
API_PATH = 'http://charette15.ing.puc.cl/api'
API_PATH_G3 = 'http://charette9.ing.puc.cl/api'

class Message(Resource):
    API_PATH_M = API_PATH + '{}'.format('/messages/{}')
    API_PATH_M_G3 = API_PATH_G3 + '{}'.format('/posts/{}')

    def get(self, id_):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_M_G3.format(id_), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            resp = resp.json()
            # La API de ellos no devuelve ni el postId ni el personId
            resp['description'] = resp['content']
            return jsonify(resp)
        else:
            abort(resp.status_code)

    def delete(self, id_):
        token = request.args.get('access_token','')
        resp = requests.delete(self.API_PATH_M_G3.format(id_), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            # Borramos el mensaje tambien en nuestra API? El id no va a calzar...
            requests.delete(self.API_PATH_M.format(id_), params={'access_token': token})
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class MessagesResponsesCollection(Resource):
    API_PATH_MRC = API_PATH + '{}'.format('/messages/{}/responses')
    API_PATH_MRC_G3 = API_PATH_G3 + '{}'.format('/posts/{}/answers')

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
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_MRC_G3.format(id_), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            resp = resp.json()
            # Acá tambien faltaría el personId
            for answer in resp:
                answer['description'] = answer['content']
                answer['messageId'] = answer['post_id']
            return jsonify(resp)
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = self.reqparse.parse_args()
        # Nosotros solo enviamos la description en los args
        # La API G3 tambien pide el user_id y el post_identifier
        argsG3 = args.copy()
        argsG3['content'] = argsG3['description']
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_MRC_G3.format(id_), data=argsG3, headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            # Tambien creamos la response en el nuestro?
            requests.post(self.API_PATH_MRC.format(id_), data=args, params={'access_token': token})
            # Aqui tambien falta personId
            resp = resp.json()
            resp['description'] = resp['content']
            resp['messageId'] = resp['post_id']
            return jsonify(resp)
        else:
            abort(resp.status_code)

g3_messages_api = Blueprint('resources_g3.messages', __name__)

api = Api(g3_messages_api)
api.add_resource(Message, '/messages/<int:id_>')
api.add_resource(MessagesResponsesCollection, '/messages/<int:id_>/responses')


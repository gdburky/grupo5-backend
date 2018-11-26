from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

API_PATH_G3 = 'http://charette9.ing.puc.cl/api'


class Message(Resource):
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
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class MessagesResponsesCollection(Resource):
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
            messages = []
            print(resp.json())
            for message in resp.json():
                item = requests.get(self.API_PATH_MRC_G3+'/{}'.format(id_, message['answer_id']),
                                   headers={'Authorization': 'Bearer ' + token})
                if item.status_code == 200:
                    item = item.json()
                    item = item[0]
                    item['content'] = item['content']
                    item['reply_id'] = item['answer_id']
                    item['author_id'] = item['user_id']
                    item['author_name'] = ""
                    item['published_at'] = item['pub_date']
                    messages.append(item)
                else:
                    abort(item.status_code)

            return jsonify(messages)
        else:
            abort(resp.status_code)



    def post(self, id_):
        args = self.reqparse.parse_args()
        # Nosotros solo enviamos la description en los args
        # La API G3 tambien pide el user_id y el post_identifier
        argsG3 = args.copy()
        argsG3['content'] = argsG3['description']
        token = request.args.get('access_token','')
        user = requests.get(API_PATH_G3 + '/user', headers={'Authorization': 'Bearer ' + token})
        resp = requests.post(self.API_PATH_MRC_G3.format(id_), data=argsG3, headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            message = resp.json()
            print(message)
            message = message[0]
            message['reply_id'] = message['answer_id']
            message['published_at'] = ""
            message['author_name'] = user.json()['username']
            message['author_id'] = user.json()['id']
            message['content'] = argsG3['description']
            return jsonify(message)
        else:
            abort(resp.status_code)

g3_messages_api = Blueprint('resources_g3.messages', __name__)

api = Api(g3_messages_api)
api.add_resource(Message, '/messages/<int:id_>')
api.add_resource(MessagesResponsesCollection, '/messages/<int:id_>/responses')


from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests


API_PATH = 'https://charette9.ing.puc.cl/api'

class Post(Resource):
    API_PATH_P = API_PATH + '{}'.format('/topics')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'description',
            required=True,
            help= 'No description provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_P, headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self):
        token = request.args.get('access_token','')
        args = self.reqparse.parse_args()
        args['title'] = args['description']
        resp = requests.post(self.API_PATH_P, headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 201:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PostMessages(Resource):
    API_PATH_PM = API_PATH + '{}'.format('/topics/{}/posts')

    def get(self, _id):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PM.format(_id), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            messages = []
            for message in resp.json():
                item = request.get(API_PATH + '/posts/{}'.format(message['id']),
                                   headers={'Authorization': 'Bearer ' + token})
                if item.status_code == 200:
                    item = item.json()
                    item['description'] = item['content']
                    item['postId'] = item['id']
                    item['personId'] = _id
                    messages.append(item)
                else:
                    abort(item.status_code)

            return jsonify(messages)
        else:
            abort(resp.status_code)

g3_posts_api = Blueprint('resources_g3.posts', __name__)

api = Api(g3_posts_api)
api.add_resource(Post, '/posts')
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
        self.reqparse.add_argument(
            'title',
            required=True,
            help= 'No title provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_P, headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            posts = []
            for post in resp.json():
                post["serviceId"] = 181
                post["personId"] = 0
                post["id"] = post["topic_id"]
                posts.append(post)
            return jsonify(posts)
        else:
            abort(resp.status_code)

    def post(self):
        token = request.args.get('access_token','')
        args = self.reqparse.parse_args()
        print(args)
        args['description'] = args['description']
        args['title'] = args['title']
        resp = requests.post(self.API_PATH_P, data=args,headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200 or resp.status_code == 201:

            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PostMessages(Resource):
    API_PATH_PM = API_PATH + '{}'.format('/topics/{}/posts')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'description',
            required=True,
            help= 'No content provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self, _id):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PM.format(_id), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            messages = []
            for message in resp.json():
                item = requests.get(API_PATH + '/posts/{}'.format(message['post_id']),
                                   headers={'Authorization': 'Bearer ' + token})
                if item.status_code == 200:

                    item = item.json()
                    item['description'] = item['content']
                    item['id'] = item['post_id']
                    item['personId'] = item['user_id']
                    item['postId'] = _id
                    messages.append(item)
                else:
                    abort(item.status_code)

            return jsonify(messages)
        else:
            abort(resp.status_code)

    def post(self, _id):
        token = request.args.get('access_token','')
        user = requests.get(API_PATH + '/user', headers={'Authorization': 'Bearer ' + token})
        if user.status_code == 200:
            args = self.reqparse.parse_args()
            data = {'user_id': user.json()['id'],'content': args['description']}
            resp = requests.post(API_PATH + '/posts',data=data, headers={'Authorization': 'Bearer ' + token})
            if resp.status_code == 200:
                data = {'topic_identifier': _id, 'post_id': resp.json()['post_id']}
                resp1 = requests.post(self.API_PATH_PM.format(_id), data=data, headers={'Authorization': 'Bearer ' + token})
                if resp1.status_code == 200:
                    message = resp1.json()
                    message['description'] = args['description']
                    message['postId'] = _id
                    message['personId'] = user.json()['id']
                    message['id'] = message['post_id']
                    return jsonify(message)
                else:
                    abort(resp1.status_code)
            else:
                abort(resp.status_code)
        else:
            abort(user.status_code)

class PostId(Resource):
    API_PATH_PI = API_PATH + '{}'.format('/topics/{}')

    def get(self, _id):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PI.format(_id), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            post = resp.json()
            post['content'] = post['description']
            post['personId'] = 0
            post['serviceId'] = 181
            post['id'] = post['topic_id']
            return jsonify(resp.json())
        else:
            abort(resp.status_code)



g3_posts_api = Blueprint('resources_g3.posts', __name__)

api = Api(g3_posts_api)
api.add_resource(Post, '/posts')
api.add_resource(PostMessages, '/posts/<int:_id>/messages')
api.add_resource(PostId, '/posts/<int:_id>')

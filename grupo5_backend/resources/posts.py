from flask import Blueprint, abort, request
from flask_restful import Resource, Api

import requests

API_PATH = 'charette15.ing.puc.cl/api'


class PostCollection(Resource):
    API_PATH_PC = API_PATH + '{}'.format('/posts')

    def get(self):
        resp = requests.get(self.API_PATH_PC)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)
    
    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PC, data=args)
        if resp.status_code == 201:
            return resp.text
        else:
            abort(resp.status_code)

class Post(Resource):
    API_PATH_P = API_PATH + '{}'.format('/posts/{}')

    def get(self, id_):
        resp = requests..get(self.API_PATH_P.format(id_))
        if resp..status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)
    
    def delete(self, id_):
        resp = requests.delete(self.API_PATH_P.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PostMessagesCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/posts/{}/messages')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PMC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PMC.format(id_), data=args)
        if resp.status_code == 201:
            return resp.text
        else:
            abort(resp.status_code)


class PostSubscriptionCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/posts/{}/subscriptions')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PSC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


class PostHashtagCollection(Resource):
    API_PATH_PHC = API_PATH + '{}'.format('posts/filter/{}')

    def get(self, hashtag):
        resp = requests.get(self.API_PATH_PHC.format(hashtag))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


posts_api = Blueprint('resources.posts', __name__)

api = Api(posts_api)
api.add_resource(PostCollection, '/posts')
api.add_resource(Post, '/posts/<int:id_>')
api.add_resource(PostMessagesCollection, '/posts/<int:id_>/messages')
api.add_resource(PostSubscriptionCollection, '/posts/<int:id_>/subscriptions')
api.add_resource(PostHashtagCollection, '/posts/filter/<string:hashtag>')

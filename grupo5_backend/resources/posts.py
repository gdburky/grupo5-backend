from flask import Blueprint, abort, request
from flask_restful import Resource, Api

import requests

API_PATH = 'charette15.ing.puc.cl/api'


class PostCollection(Resource):
    API_PATH_PC = API_PATH + '{}'.format('/services/{}/posts')

    def get(self, apiKey):
        resp = requests.get(self.API_PATH_PC.format(apiKey))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class Post(Resource):
    API_PATH_P = API_PATH + '{}'.format('/services/{}/posts/{}')
    API_PATH_P_CREATE = API_PATH + '{}'.format('/services/{}/posts/author/{}')

    def post(self, apiKey, id_):
        args = request.form
        resp = requests.post(self.API_PATH_P_CREATE.format(apiKey, id_), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def get(self, apiKey, id_):
        resp = requests.get(self.API_PATH_P.format(apiKey, id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def put(self, apiKey, id_):
        resp = requests.put(self.API_PATH_P.format(apiKey, id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def delete(self, apiKey, id_):
        resp = requests.delete(self.API_PATH_P.format(apiKey, id_))
        if resp.status_code == 204:
            return resp.text
        else:
            abort(resp.status_code)  

class PostMessagesCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/services/{}/posts/{}/messages')

    def get(self, apiKey, id_):
        resp = requests.get(self.API_PATH_PMC.format(apiKey, id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PostSubscriptionCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/services/{}/posts/{}/subscriptions')

    def get(self, apiKey, id_):
        resp = requests.get(self.API_PATH_PSC.format(apiKey, id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


class PostHashtagCollection(Resource):
    API_PATH_PHC = API_PATH + '{}'.format('/services/{}/posts/filter/{}')

    def get(self, apiKey, hashtag):
        resp = requests.get(self.API_PATH_PHC.format(apiKey, hashtag))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


posts_api = Blueprint('resources.posts', __name__)

api = Api(posts_api)
api.add_resource(PostCollection, '/services/<int:apiKey>/posts')
api.add_resource(Post, '/services/<int:apiKey>/posts/<int:id_>')
api.add_resource(Post, '/services/<int:apiKey>/posts/author/<int:id_>')
api.add_resource(PostMessagesCollection, '/services/<int:apiKey>/posts/<int:id_>/messages')
api.add_resource(PostSubscriptionCollection, '/services/<int:apiKey>/posts/<int:id_>/subscriptions')
api.add_resource(PostHashtagCollection, '/services/<int:apiKey>/posts/filter/<string:hashtag>')

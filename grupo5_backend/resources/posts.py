from flask import Blueprint
from flask_restful import Resource, Api

import requests

API_PATH = 'charette15.ing.puc.cl'

class PostCollection(Resource):
    API_PATH_POSTCOLLECTION = API_PATH + '{}'.format('/posts')

    def get(self):
        return requests.get(self.API_PATH_POSTCOLLECTION)

    def post(self):
        context = {}
        return requests.post(self.API_PATH_POSTCOLLECTION, data=context)


class Post(Resource):
    API_PATH_POST = API_PATH + '{}'.format('/post/{}')

    def get(self, id):
        return requests.get(self.API_PATH_POST.format(id))

class PostSubscriptorCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/post/{}/subscriptors')

    def get(self, id):
        return requests.get(self.API_PATH_PSC.format(id))


posts_api = Blueprint('resources.posts', __name__)

api = Api(posts_api)
api.add_resource(PostCollection, '/posts')
api.add_resource(Post, '/post/<int:id>')
api.add_resource(PostSubscriptorCollection, '/post/<int:id>/subscriptors')





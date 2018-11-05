from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

from resources.service import serviceId

API_PATH = 'http://charette15.ing.puc.cl/api'

class PostCollection(Resource):
   API_PATH_PC = API_PATH + '{}'.format('/services/{}/posts')

   def get(self):
       global serviceId
       params = request.args.get('access_token','')
       resp = requests.get(self.API_PATH_PC.format(serviceId), params={'access_token': params})
       if resp.status_code == 200:
           return jsonify(resp.json())
       else:
           abort(resp.status_code)

class Post(Resource):
    API_PATH_P = API_PATH + '{}'.format('/services/{}/posts/{}')
    API_PATH_P2 = API_PATH + '{}'.format('/posts/{}')

    def get(self, id_):
        params = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_P2.format(id_), params={'access_token': params})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def put(self, id_):
        global serviceId
        resp = requests.put(self.API_PATH_P.format(serviceId, id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def delete(self, id_):
        global serviceId
        resp = requests.delete(self.API_PATH_P.format(serviceId, id_))
        if resp.status_code == 204:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PostCreate(Resource):
    API_PATH_P_CREATE = API_PATH + '{}'.format('/services/{}/posts')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'description',
            required=True,
            help= 'No description provided',
            location=['form', 'json',]
        )
        super().__init__()

    def post(self):
        global serviceId
        params = request.args.get('access_token','')
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_P_CREATE.format(serviceId), data=args, params={'access_token': params})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PostMessagesCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/services/{}/posts/{}/messages')

    def get(self, id_):
        global serviceId
        params = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PMC.format(serviceId, id_), params = request.args.get('access_token',''))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PostSubscriptionCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/services/{}/posts/{}/subscriptions')

    def get(self, id_):
        global serviceId
        resp = requests.get(self.API_PATH_PSC.format(serviceId, id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


class PostHashtagCollection(Resource):
    API_PATH_PHC = API_PATH + '{}'.format('/services/{}/filterPosts/filterString')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'hashtag',
            required=True,
            help= 'No hashtag provided',
            location=['form', 'json',]
        )
        super().__init__()

    def get(self):
        global serviceId
        params = request.args.get('access_token','')
        args = self.reqparse.parse_args()
        resp = requests.get(self.API_PATH_PHC.format(serviceId), data=args, params={'access_token': params})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


posts_api = Blueprint('resources.posts', __name__)

api = Api(posts_api)
api.add_resource(PostCollection, '/posts')
api.add_resource(Post, '/posts/<int:id_>')
api.add_resource(PostCreate, '/posts', endpoint='postcreate')
api.add_resource(PostMessagesCollection, '/posts/<int:id_>/messages')
api.add_resource(PostSubscriptionCollection, '/posts/<int:id_>/subscriptions')
api.add_resource(PostHashtagCollection, '/filterPosts/filterString')



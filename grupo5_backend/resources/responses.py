from flask import Blueprint, abort, request
from flask_restful import Resource, Api

import requests

API_PATH = 'http://charette15.ing.puc.cl/api'


class ResponseCollection(Resource):
    API_PATH_RC = API_PATH + '{}'.format('/responses')

    def get(self):
        resp = requests.get(self.API_PATH_RC)
        if resp.status_code == 200:
            return resp.text
        else: 
            abort(resp.status_code)

class Response(Resource):
    API_PATH_R = API_PATH + '{}'.format('/services/{}/posts/{}/messages/{}/responses/{}')
    API_PATH_R_CREATE = API_PATH + '{}'.format('/services/{}/posts/{}/messages/{}/responses/author/{}')

    def post(self, apiKey, postId, msgId, id_):
        args = request.form
        resp = requests.post(self.API_PATH_R_CREATE.format(apiKey, postId, msgId, id_), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def get(self, apiKey, postId, msgId, id_):
        resp = requests.get(self.API_PATH_R.format(apiKey, postId, msgId, id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)
    
    def delete(self, id_):
        resp = requests.delete(self.API_PATH_R.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


responses_api = Blueprint('resources.responses', __name__)

api = Api(responses_api)
api.add_resource(ResponseCollection, '/responses')
api.add_resource(Response, '/services/<int:apiKey>/posts/<int:postId>/messages/<int:msgId>/responses/<int:id_>')
api.add_resource(Response, '/services/<int:apiKey>/posts/<int:postId>/messages/<int:msgId>/responses/author/<int:id_>', endpoint='responsecreate')

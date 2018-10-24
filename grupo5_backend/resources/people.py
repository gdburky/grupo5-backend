from flask import Blueprint, abort, request
from flask_restful import Resource, Api, reqparse

import requests

API_PATH = 'charette15.ing.puc.cl/api'

class PersonRegister(Resource):
    API_PATH_PR = API_PATH + '{}'.format('/people')

    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PR, data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonLogin(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/people/login')

    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PL, data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonLogout(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/people/logout')

    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PL, data=args)
        if resp.status_code == 204:
            return resp.text
        else:
            abort(resp.status_code)

class PersonChangePassword(Resource):
    API_PATH_PCP = API_PATH + '{}'.format('/people/change-password')

    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PCP, data=args)
        if resp.status_code == 204:
            return resp.text
        else:
            abort(resp.status_code)

class Person(Resource):
    API_PATH_P = API_PATH + '{}'.format('/services/{}/people/{}')

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

class PersonCollection(Resource):
    API_PATH_PC = API_PATH + '{}'.format('/services/{}/people')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    #este es para crear personas pero usa el mismo path PC...    
    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PC.format(id_), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonPostCollection(Resource):
    API_PATH_PPC = API_PATH + '{}'.format('/people/{}/posts')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PPC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PPC.format(id_), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonMessageCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/people/{}/messages')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PMC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PMC.format(id_), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonResponseCollection(Resource):
    API_PATH_PRC = API_PATH + '{}'.format('/people/{}/responses')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PRC.format(id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PRC.format(id_), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonSubscriptionCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/services/{}/people/{}/subscriptions')

    def get(self, apiKey, id_):
        resp = requests.get(self.API_PATH_PSC.format(apiKey, id_))
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)

class PersonSubscribePost(Resource):
    API_PATH_PSP = API_PATH + '{}'.format('/services/{}/people/{}/subscriptions/posts/{}')

    def post(self, apiKey, id_, postId):
        args = request.form
        resp = requests.post(self.API_PATH_PSP.format(apiKey, id_, postId), data=args)
        if resp.status_code == 200:
            return resp.text
        else:
            abort(resp.status_code)


person_api = Blueprint('resources.people', __name__)

api = Api(person_api)
api.add_resource(PersonRegister, '/people')
api.add_resource(PersonLogin, '/people/login')
api.add_resource(PersonLogout, '/people/logout')
api.add_resource(PersonChangePassword, '/people/change-password')
api.add_resource(Person, '/services/<int:apiKey>/people/<int:id_>')
api.add_resource(PersonCollection, 'services/<int:apiKey>/people')
api.add_resource(PersonPostCollection, '/people/<int:id_>/posts')
api.add_resource(PersonMessageCollection, '/people/<int:id_>/messages')
api.add_resource(PersonResponseCollection, '/people/<int:id_>/responses')
api.add_resource(PersonSubscriptionCollection, '/services/<int:apiKey>/people/<int:id_>/subscriptions')
api.add_resource(PersonSubscribePost, '/services/<int:apiKey>/people/<int:id_>/subscriptions/posts/<int:postId>')

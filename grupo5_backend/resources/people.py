from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

from resources.service import serviceId

API_PATH = 'http://charette15.ing.puc.cl/api'

class PersonRegister(Resource):
    API_PATH_PR = API_PATH + '{}'.format('/people')

    def post(self):
        args = request.form

        resp = requests.post(self.API_PATH_PR, data=args)
        if resp.status_code == 201:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonLogin(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/people/login')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help= 'No email provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help= 'No password provided',
            location=['form', 'json',]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_PL, data=args)
        if resp.status_code == 200:
            data = resp.json()
            global serviceId
            serviceId = data['id']
            return jsonify(data)
        else:
            abort(resp.status_code)

class PersonLogout(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/people/logout')

    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PL, data=args)
        if resp.status_code == 204:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonChangePassword(Resource):
    API_PATH_PCP = API_PATH + '{}'.format('/people/change-password')

    def post(self):
        args = request.form
        resp = requests.post(self.API_PATH_PCP, data=args)
        if resp.status_code == 204:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class Person(Resource):
    API_PATH_P = API_PATH + '{}'.format('/people/{}')

    def get(self, id_):
        args = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_P.format( id_), params={'access_token': args})
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

class PersonCollection(Resource):
    API_PATH_PC = API_PATH + '{}'.format('/services/{}/people')

    def get(self):
        global serviceId
        resp = requests.get(self.API_PATH_PC.format(serviceId))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    #este es para crear personas pero usa el mismo path PC...    
    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PC.format(id_), data=args)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonPostCollection(Resource):
    API_PATH_PPC = API_PATH + '{}'.format('/people/{}/posts')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PPC.format(id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PPC.format(id_), data=args)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonMessageCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/people/{}/messages')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PMC.format(id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PMC.format(id_), data=args)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonResponseCollection(Resource):
    API_PATH_PRC = API_PATH + '{}'.format('/people/{}/responses')

    def get(self, id_):
        resp = requests.get(self.API_PATH_PRC.format(id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        resp = requests.post(self.API_PATH_PRC.format(id_), data=args)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonSubscriptionCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/services/{}/people/{}/subscriptions')

    def get(self, id_):
        global serviceId
        resp = requests.get(self.API_PATH_PSC.format(serviceId, id_))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonSubscribePost(Resource):
    API_PATH_PSP = API_PATH + '{}'.format('/services/{}/people/{}/subscriptions/posts/{}')

    def post(self, id_, postId):
        global serviceId
        args = request.form
        resp = requests.post(self.API_PATH_PSP.format(serviceId, id_, postId), data=args)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonDeleteSubscription(Resource):
    API_PATH_DS = API_PATH + '{}'.format('/services/{}/people/{}/subscriptions/{}')

    def delete(self, id_, subId):
        global serviceId
        resp = requests.delete(self.API_PATH_S.format(serviceId, id_, subId))
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


person_api = Blueprint('resources.people', __name__)

api = Api(person_api)
api.add_resource(PersonRegister, '/people')
api.add_resource(PersonLogin, '/people/login')
api.add_resource(PersonLogout, '/people/logout')
api.add_resource(PersonChangePassword, '/people/change-password')
api.add_resource(Person, '/people/<int:id_>')
api.add_resource(PersonCollection, '/people')
api.add_resource(PersonPostCollection, '/people/<int:id_>/posts')
api.add_resource(PersonMessageCollection, '/people/<int:id_>/messages')
api.add_resource(PersonResponseCollection, '/people/<int:id_>/responses')
api.add_resource(PersonSubscriptionCollection, '/people/<int:id_>/subscriptions')
api.add_resource(PersonSubscribePost, '/people/<int:id_>/subscriptions/posts/<int:postId>')
api.add_resource(PersonDeleteSubscription, '/people/<int:id_>/subscriptions/<int:subId>')

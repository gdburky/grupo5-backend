from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests

SERVICEID = '181'
ADMIN_EMAIL = 'a@a.cl'
PASSWORD = '1234'
LOGIN_DATA = {
    'email': ADMIN_EMAIL,
    'password': PASSWORD
}
API_PATH = 'http://charette15.ing.puc.cl/api'

def getAccessToken(user):
    response = requests.post(API_PATH + '/people/login', data=user)
    return response.json()['id']


class PersonRegister(Resource):
    API_PATH_PR = API_PATH + '{}'.format('/services/{}/people')

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
        token = getAccessToken(LOGIN_DATA)
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_PR.format(SERVICEID), data=args, params={'access_token': token})
        if resp.status_code == 200:
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
            return jsonify(data)
        else:
            abort(resp.status_code)

class PersonLogout(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/people/logout')

    def post(self):
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_PL, params={'access_token': token})
        if resp.status_code == 204:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonChangePassword(Resource):
    API_PATH_PCP = API_PATH + '{}'.format('/people/change-password')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'newPassword',
            required=True,
            help= 'No newPassword provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'oldPassword',
            required=True,
            help= 'No oldPassword provided',
            location=['form', 'json',]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_PCP, data=args, params={'access_token': token})
        if resp.status_code == 204:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class Person(Resource):
    API_PATH_PERSON = API_PATH + '{}'.format('/services/{}/people/{}')
    API_PATH_P = API_PATH + '{}'.format('/people/{}')

    def get(self, id_):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PERSON.format(SERVICEID, id_), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def put(self, id_):
        token = request.args.get('access_token','')
        resp = requests.put(self.API_PATH_P.format( id_), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def delete(self, id_):
        token = request.args.get('access_token','')
        resp = requests.delete(self.API_PATH_P.format( id_), params={'access_token': token})
        if resp.status_code == 204:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonCollection(Resource):
    API_PATH_PC = API_PATH + '{}'.format('/services/{}/people')

    def get(self):
        token = getAccessToken(LOGIN_DATA)
        resp = requests.get(self.API_PATH_PC.format(SERVICEID), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    #este es para crear personas pero usa el mismo path PC...
    '''
    def post(self, id_):
        token = request.args.get('access_token','')
        args = request.form
        resp = requests.post(self.API_PATH_PC.format(id_), data=args, params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)
    '''

'''
class PersonPostCollection(Resource):
    API_PATH_PPC = API_PATH + '{}'.format('/people/{}/posts')

    def get(self, id_):
        token = getAccessToken(LOGIN_DATA)
        resp = requests.get(self.API_PATH_PPC.format(id_), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_PPC.format(id_), data=args, params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonMessageCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/people/{}/messages')

    def get(self, id_):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PMC.format(id_), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        token = request.args.get('access_token','')
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
'''

class PersonSubscriptionCollection(Resource):
    API_PATH_PSC = API_PATH + '{}'.format('/people/{}/subscriptions')

    def get(self, id_):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PSC.format( id_), params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

    def post(self, id_):
        args = request.form
        token = request.args.get('access_token','')
        resp = requests.post(self.API_PATH_PSC.format( id_), data=args, params={'access_token': token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

'''
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
'''

class PersonSubscription(Resource):
    API_PATH_DS = API_PATH + '{}'.format('/people/{}/subscriptions/{}')

    def delete(self, id_, subId):
        token = request.args.get('access_token','')
        resp = requests.delete(self.API_PATH_DS.format( id_, subId), params={'access_token': token})
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
#api.add_resource(PersonPostCollection, '/people/<int:id_>/posts')
#api.add_resource(PersonMessageCollection, '/people/<int:id_>/messages')
#api.add_resource(PersonResponseCollection, '/people/<int:id_>/responses')
api.add_resource(PersonSubscriptionCollection, '/people/<int:id_>/subscriptions')
api.add_resource(PersonSubscription, '/people/<int:id_>/subscriptions/<int:subId>')
#api.add_resource(PersonSubscribePost, '/people/<int:id_>/subscriptions/posts/<int:postId>')

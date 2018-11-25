from flask import Blueprint, abort, request, jsonify
from flask_restful import Resource, Api, reqparse

import requests


API_PATH = 'https://charette9.ing.puc.cl/api'

class PersonRegister(Resource):
    API_PATH_PR = API_PATH + '{}'.format('/users')

    def __init__(self):
        self.reqparse= reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help= 'No email provided',
            location=['form', 'json', ]
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help= 'No password provided',
            location=['form', 'json',]
        )
        self.reqparse.add_argument(
            'username',
            required=True,
            help= 'No username provided',
            location=['form', 'json',]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        resp = requests.post(self.API_PATH_PR, data=args)
        print(resp.status_code)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


    def get(self):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PR, headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)


class PersonLogin(Resource):
    API_PATH_PL = API_PATH + '{}'.format('/login')

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
            location=['form', 'json', ]
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        resp = requests.post(self.API_PATH_PL, data=args)
        if resp.status_code == 200:
            data = {'id': resp.json()['token']}
            data['userId'] = resp.json()['user']['id']
            return jsonify(data)
        else:
            abort(resp.status_code)

class PersonId(Resource):
    API_PATH_PI = API_PATH + '{}'.format('/users/{}')

    def get(self, _id):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PI.format(_id), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            abort(resp.status_code)

class PersonPostCollection(Resource):
    API_PATH_PPC = API_PATH + '{}'.format('/users/{}/topics')

    def get(self, _id):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PPC.format(_id), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            posts = []
            for post in resp.json():
                item = request.get(API_PATH + '/topics/{}'.format(post['id']),
                                   headers={'Authorization': 'Bearer ' + token})
                if item.status_code == 200:
                    item = item.json()
                    item['personId'] = _id
                    posts.append(item)
                else:
                    abort(item.status_code)

            return jsonify(posts)
        else:
            abort(resp.status_code)

class PersonMessagesCollection(Resource):
    API_PATH_PMC = API_PATH + '{}'.format('/users/{}/topics')

    def get(self, _id):
        token = request.args.get('access_token','')
        resp = requests.get(self.API_PATH_PMC.format(_id), headers={'Authorization': 'Bearer ' + token})
        if resp.status_code == 200:
            messages = []
            for message in resp.json():
                item = request.get(API_PATH + '/posts/{}'.format(message['id']),
                                   headers={'Authorization': 'Bearer ' + token})
                if item.status_code == 200:
                    item = item.json()
                    item['personId'] = _id
                    messages.append(item)
                else:
                    abort(item.status_code)

            return jsonify(messages)
        else:
            abort(resp.status_code)




g3_person_api = Blueprint('resources_g3.people', __name__)

api = Api(g3_person_api)
api.add_resource(PersonRegister, '/people')
api.add_resource(PersonLogin, '/people/login')
api.add_resource(PersonId, '/people/<int:_id>')
#api.add_resource(PersonPostCollection, '/people/<int:_id>/posts')
#api.add_resource(PersonMessagesCollection, '/people/<int:_id>/messages')




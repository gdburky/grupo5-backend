import logging

from flask import request
from flask_restplus import Resource

from grupo5_backend.api.blog.business import create_blog_post, update_post, delete_post # TODO: cambiar para user
from grupo5_backend.api.blog.serializers import blog_post, page_of_blog_posts # TODO: cambiar para user

from grupo5_backend.api.blog.parsers import pagination_arguments
from grupo5_backend.api.restplus import api
from grupo5_backend.database.models import Post

log = logging.getLogger(__name__)

ns = api.namespace('users', description='Operations related users')


@ns.route('/')
class UsersCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_blog_posts) # TODO: cambiar para user
    def get(self):
        """
        Returns list of users.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        users_query = User.query
        users_page = users_query.paginate(page, per_page, error_out=False)

        return users_page

    @api.expect(user)
    def post(self):
        """
        Creates a new user.
        """
        create_blog_post(request.json) # TODO: cambiar para user
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'User not found.')
class UserItem(Resource):

    @api.marshal_with(user)
    def get(self, id):
        """
        Returns a  user.
        """
        return User.query.filter(User.id == id).one()

    @api.expect(user)
    @api.response(204, 'User successfully updated.')
    def put(self, id):
        """
        Updates a usert.
        """
        data = request.json
        update_post(id, data) # TODO: cambiar para user
        return None, 204


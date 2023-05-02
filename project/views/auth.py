from flask_restx import abort, Namespace, Resource
from flask import request

from project.tools.security import login_user, refresh_user_token
from project.exceptions import ItemNotFound
from project.services.users_service import UsersService
from project.setup_db import db

auth_ns = Namespace('auth')
secret = 's3cR$eT'
algo = 'HS256'


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get("email", None)
        password = req_json.get("password", None)
        if None in [email, password]:
            abort(400)
        try:
            user = UsersService(db.session).get_item_by_email(email=email)
            tokens = login_user(request.json, user)
            return tokens, 201
        except ItemNotFound:
            abort(401, "ошибка авторизации")

    def put(self):
        req_json = request.json
        if None in req_json:
            abort(400)

        try:
            tokens = refresh_user_token(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, "ошибка авторизации")

@auth_ns.route('/register')
class AuthRegView(Resource):
    def post(self):
        req_json = request.json
        if None in req_json:
            abort(400, "не корректный запрос")
        return UsersService(db.session).create(req_json)




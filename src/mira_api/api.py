# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
import graphene
from .schemas.query import Query
from .schemas.mutation import Mutation
from .database import db_session
from .models.auth import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity,
    create_refresh_token, jwt_refresh_token_required
)
from .login import LoginAPI, Status

SECRET_KEY = "\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"

APP = Flask(__name__)
APP.config["JWT_SECRET_KEY"] = SECRET_KEY
JWT = JWTManager(APP)
CORS(APP)
SCHEMA = graphene.Schema(query=Query, mutation=Mutation)


class SecureGraphQL(GraphQLView):

    @jwt_required
    def dispatch_request(self, *args, **kwargs):
        return super(SecureGraphQL, self).dispatch_request(*args, **kwargs)

APP.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=SCHEMA, graphiql=True)
)
APP.add_url_rule(
    '/login',
    view_func=LoginAPI.as_view("login")
)
APP.add_url_rule(
    '/status',
    view_func=Status.as_view("status")
)


@APP.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        "access_token": create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@APP.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

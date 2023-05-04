from functools import wraps
from flask import Blueprint, request, session, make_response, jsonify
from src.models.users import User
from src.types.user_type import userInput
from ..error import errors
from ast import literal_eval

userAuthRoutes = Blueprint("userAuth", __name__)


@userAuthRoutes.route("/user/login", methods=["Post"])
def login():
    data = literal_eval(request.data.decode("utf-8"))
    user: User = User.login(userLoginInput=data)
    session["user_id"] = user["id"]
    return make_response(jsonify(user.as_dict()), 200)


@userAuthRoutes.route("/user/new", methods=["POST"])
def newUser():
    data = literal_eval(request.data.decode("utf-8"))
    user = User.newUser(data)
    session["user_id"] = user["id"]
    return make_response(jsonify(dict(user)), 200)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "user_id" in session:
            return f(*args, **kwargs)
        else:
            raise errors.HTTPError(code=401)

    return wrap


@userAuthRoutes.route("/user/logout", methods=["POST"])
@login_required
def logout():
    session.pop("user_id", None)
    return make_response(jsonify({}), 200)

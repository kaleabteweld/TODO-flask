from functools import wraps
from flask import Blueprint, request, session, make_response, jsonify
from ..error import errors
from werkzeug.security import check_password_hash, generate_password_hash
from ast import literal_eval

userAuthRoutes = Blueprint("userAuth", __name__)


@userAuthRoutes.route("/user/login", methods=["Post"])
def login():
    data = request.form
    session["user_id"] = data["user_id"]
    return make_response(jsonify({"user_id": data["user_id"]}), 200)


@userAuthRoutes.route("/user/new", methods=["POST"])
def newUser():
    data = literal_eval(request.data.decode("utf-8"))
    print(data)
    session["user_id"] = data["user_id"]
    return make_response(jsonify(data), 200)


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

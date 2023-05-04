from flask import Blueprint, request, make_response, jsonify, session
from json import JSONDecoder

from .auth import login_required


userRoutes = Blueprint("user", __name__)


@userRoutes.route("/<user_id>", methods=["GET"])
def getUser(user_id: str):
    response = make_response(jsonify({"user_id": user_id}), 200)
    return response


@userRoutes.route("/me", methods=["GET"])
@login_required
def me():
    user_id = session["user_id"]
    response = make_response(jsonify({"user_id": user_id}), 200)
    return response

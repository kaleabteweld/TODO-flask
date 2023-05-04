from flask import Blueprint, request, make_response, jsonify, session
from json import JSONDecoder
from src.models.todo import Todo
from src.models.users import User
from src.types.types import Pagination
from .auth import login_required


userRoutes = Blueprint("user", __name__)


# @userRoutes.route("/<user_id>", methods=["GET"])
# def getUser(user_id: str):
#     response = make_response(jsonify({"user_id": user_id}), 200)
#     return response


@userRoutes.route("/me", methods=["GET"])
@login_required
def me():
    user_id = session["user_id"]
    user: User = User.getUserById(id=user_id)
    response = make_response(jsonify(user.as_dict()), 200)
    return response


@userRoutes.route("/me/todos", methods=["GET"])
@login_required
def getTodos():
    limit = request.args.get("limit")
    offset = request.args.get("offset")

    user_id = session["user_id"]
    todos = Todo.getUserTodos(
        id=user_id, pagination=Pagination(limit=limit, offset=offset)
    )

    mappedTodos = list(map(lambda todo: todo.as_dict(), todos))
    response = make_response(jsonify(mappedTodos), 200)
    return response

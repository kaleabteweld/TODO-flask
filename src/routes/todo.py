from ast import literal_eval
from flask import Blueprint, request, jsonify, session

from src.models.todo import Todo
from .auth import login_required


todoRoutes = Blueprint("todo", __name__)


@todoRoutes.route("/new", methods=["POST"])
@login_required
def newTodo():
    data = literal_eval(request.data.decode("utf-8"))
    user_id = session["user_id"]

    todo: Todo = Todo.newTodo(todoInput=data, user_id=user_id)
    return jsonify(todo.as_dict())


@todoRoutes.route("/delete/<id>", methods=["DELETE"])
@login_required
def deleteTodo(id: str):
    Todo.deleteTodoById(id=id)
    return jsonify({"message": "Todo deleted successfully"})


@todoRoutes.route("/updata/<id>", methods=["PATCH"])
@login_required
def updateTodo(id: str):
    data = literal_eval(request.data.decode("utf-8"))
    newTodo = Todo.updateTodoById(id=id, todoInput=data)
    return jsonify(newTodo.as_dict())

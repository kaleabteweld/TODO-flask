from flask import Flask
from . import user, auth, todo


def registerRoutes(app: Flask):
    app.register_blueprint(user.userRoutes, url_prefix="/user")
    app.register_blueprint(auth.userAuthRoutes, url_prefix="/auth")
    app.register_blueprint(todo.todoRoutes, url_prefix="/todo")

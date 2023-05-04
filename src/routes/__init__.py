from flask import Flask


def registerRoutes(app: Flask):
    from . import user, auth

    app.register_blueprint(user.userRoutes, url_prefix="/user")
    app.register_blueprint(auth.userAuthRoutes, url_prefix="/auth")

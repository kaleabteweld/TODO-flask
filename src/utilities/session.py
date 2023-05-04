from flask import Flask
from src.utilities.consts import sess, db
import redis


def initSession(app: Flask, sessionType: str = "redis"):
    _app = app
    if sessionType == "redis":
        _app = redisSessioninit(app)
    elif sessionType == "sqlalchemy":
        _app = sqlSessionInit(app)

    sess.init_app(_app)

    return _app


def redisSessioninit(app: Flask):
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = redis.from_url("redis://localhost:6379")

    return app


def sqlSessionInit(app: Flask):
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db

    return app

from flask import Flask, jsonify
from .errors import HTTPError


def addRoutesErrorsHandled(app: Flask):

    @app.errorhandler(404)
    def resoure_not_found(error):
        return jsonify(error), 404

    # @app.errorhandler(Exception)
    # def special_exception_handler(error):
    #     return 'Database connection failed', 500

    @app.errorhandler(HTTPError)
    def http_error(error: HTTPError):
        return error.message, error.code

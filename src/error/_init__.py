from flask import Flask, jsonify
from nbformat import ValidationError
from .errors import HTTPError


def addRoutesErrorsHandled(app: Flask):
    @app.errorhandler(404)
    def resoure_not_found(error):
        return jsonify(error), 404

    @app.errorhandler(HTTPError)
    def http_error(error: HTTPError):
        return jsonify({"error": error.message}), error.code

    @app.errorhandler(ValidationError)
    def validation_error(error: ValidationError):
        return jsonify({"error": error.message, "path": "".join(error.path)}), 400

    @app.errorhandler(Exception)
    def exception_handler(error):
        return str(error), 500

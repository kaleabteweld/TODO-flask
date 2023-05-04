import http.client
from typing import Union


class HTTPError(Exception):
    def __init__(self, code, message: Union[str, None] = None):
        Exception.__init__(self)
        self.code = code

        if message is None:
            self.message = http.client.responses[code]
        else:
            self.message = message

    def to_dict(self):
        return {"message": self.message, "code": self.code}

    def __str__(self):
        return f"{self.message} {self.code}"


class SqlAlchemyError(Exception):
    def __init__(self, exception: Exception, message: Union[str, None] = None):
        Exception.__init__(self)
        self.message = message

        if message is None:
            self.message = str(exception)

    def to_dict(self):
        return {"message": self.message, "code": 500}

    def __str__(self):
        return f"{self.message} 500"

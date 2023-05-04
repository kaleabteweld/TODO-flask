from functools import wraps
import sqlite3

from nbformat import ValidationError
import sqlalchemy
from src.error.errors import SqlAlchemyError


def query(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print("Query Error", e)
            if isinstance(e, ValidationError):
                raise e
            if isinstance(e, sqlite3.IntegrityError) or isinstance(
                e, sqlalchemy.exc.IntegrityError
            ):
                raise ValidationError(
                    message=str(e).split(":")[0].split(")")[1].strip(),
                    path=str(e).split(":")[1],
                )
            raise SqlAlchemyError(e)

    return wrap

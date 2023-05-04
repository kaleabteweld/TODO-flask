from functools import wraps
import sqlite3
from typing import TypeVar
from voluptuous import Schema, MultipleInvalid
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


T = TypeVar("T")


def validation(schema: Schema, input: any) -> T:
    try:
        schema(input)
        return input
    except MultipleInvalid as e:
        e = str(e)
        validation_error = e.split(" @ ")[0]
        key_name = e.split(" @ ")[1].split("['")[1].split("']")[0]
        raise ValidationError(message=validation_error, path=key_name)

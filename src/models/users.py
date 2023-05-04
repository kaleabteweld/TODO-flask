import uuid
from jsonschema import Validator
from nbformat import ValidationError
from pyparsing import Any
from src.types.user_type import userInput
from .validation import user_validation

from src.utilities.fun import query
from ..utilities.consts import db
from sqlalchemy.sql import func, select, and_
from werkzeug.security import check_password_hash, generate_password_hash

from voluptuous import MultipleInvalid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4().hex)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    @query
    def login(userLoginInput: dict[Any, Any]):
        try:
            user_validation.user_login_validation_schema(userLoginInput)
        except MultipleInvalid as e:
            e = str(e)
            validation_error = e.split(" @ ")[0]
            key_name = e.split(" @ ")[1].split("['")[1].split("']")[0]
            raise ValidationError(message=validation_error, path=key_name)

        user = db.session.query(User).filter_by(email=userLoginInput["email"]).first()

        if user is None:
            raise ValidationError("Incorrect password or email")
        if not check_password_hash(user.password_hash, userLoginInput["password"]):
            raise ValidationError("Incorrect password", path="password")

        return user

    @query
    def getUserByUsername(self, username):
        return self.query.filter_by(username=username).first()

    @query
    def getUserById(self, id):
        return self.query.filter_by(id=id).first()

    @staticmethod
    @query
    def newUser(userInput: dict[Any, Any]):
        try:
            user_validation.user_validation_schema(userInput)
        except MultipleInvalid as e:
            e = str(e)
            validation_error = e.split(" @ ")[0]
            key_name = e.split(" @ ")[1].split("['")[1].split("']")[0]
            raise ValidationError(message=validation_error, path=key_name)

        print("userInput ", userInput)
        user: User = User(username=userInput["username"], email=userInput["email"])
        user.set_password(userInput["password"])

        db.session.add(user)
        db.session.commit()
        print("User created", user)
        return user

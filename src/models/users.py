import uuid
from jsonschema import Validator
from nbformat import ValidationError
from pyparsing import Any
from src.types.user_type import userInput
from .validation import user_validation
from sqlalchemy import func, Column, String, DateTime, Enum, ForeignKey
from src.utilities.fun import query
from ..utilities.consts import db
from werkzeug.security import check_password_hash, generate_password_hash
from src.utilities import fun


from voluptuous import MultipleInvalid


class User(db.Model):
    __tablename__ = "users"

    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    @query
    def login(userLoginInput: dict[Any, Any]):
        fun.validation(
            schema=user_validation.user_login_validation_schema, input=userLoginInput
        )

        user = User.query.filter_by(email=userLoginInput["email"]).first()

        if user is None:
            raise ValidationError("Incorrect password or email")
        if not check_password_hash(user.password_hash, userLoginInput["password"]):
            raise ValidationError("Incorrect password", path="password")

        return user

    @staticmethod
    @query
    def getUserByUsername(self, username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    @query
    def getUserById(id):
        user = User.query.filter_by(id=id).first()
        return user

    @staticmethod
    @query
    def newUser(userInput: dict[Any, Any]):
        fun.validation(schema=user_validation.user_validation_schema, input=userInput)

        user: User = User(username=userInput["username"], email=userInput["email"])
        user.set_password(userInput["password"])

        db.session.add(user)
        db.session.commit()
        return user

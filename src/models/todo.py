import uuid
from nbformat import ValidationError
from pyparsing import Any
from sqlalchemy import func, Column, String, DateTime, Enum, ForeignKey
from src.types.types import Pagination, StatusEnum
from src.utilities import fun
from src.utilities.fun import query
from ..utilities.consts import db
from .validation import todo_validation


class Todo(db.Model):
    __tablename__ = "todos"

    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = Column(String(80), nullable=False)
    description = Column(String(120), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(StatusEnum), default=StatusEnum.onGoing)
    user_id = Column(String(80), ForeignKey("users.id"), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @query
    def newTodo(todoInput: dict[Any, Any], user_id: str):
        fun.validation(schema=todo_validation.new_todo_schema, input=todoInput)

        todo = Todo(
            title=todoInput["title"],
            description=todoInput["description"],
            user_id=user_id,
        )
        db.session.add(todo)
        db.session.commit()
        return todo

    @query
    def getUserTodos(id: str, pagination: Pagination) -> list:
        return (
            Todo.query.filter_by(user_id=id)
            .limit(pagination.limit)
            .offset(pagination.offset)
            .all()
        )

    @staticmethod
    @query
    def getTodoById(id: str):
        todo = Todo.query.filter_by(id=id).first()
        if todo is None:
            raise ValidationError("Todo not found", path="id")
        return todo

    @staticmethod
    @query
    def deleteTodoById(id: str):
        todo = Todo.getTodoById(id=id)
        db.session.delete(todo)
        db.session.commit()
        return todo

    @staticmethod
    @query
    def updateTodoById(id: str, todoInput: dict[Any, Any]):
        fun.validation(schema=todo_validation.update_todo_schema, input=todoInput)

        todo = Todo.getTodoById(id=id)
        todo = Todo.compareAndUpdate(todo=todo, todoInput=todoInput)

        db.session.commit()
        return todo

    @staticmethod
    def compareAndUpdate(todo, todoInput: dict[Any, Any]):
        for key, value in todoInput.items():
            if value is not None and value != getattr(todo, key):
                setattr(todo, key, value)
        return todo

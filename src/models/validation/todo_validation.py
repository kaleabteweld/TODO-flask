from voluptuous import Schema, Length, Email, In, Optional
from src.types.types import StatusEnum

new_todo_schema = Schema(
    {
        "title": Length(min=8, max=50),
        "description": Length(min=8, max=100),
    },
    required=True,
)


update_todo_schema = Schema(
    {
        Optional("title"): Length(min=8, max=50),
        Optional("description"): Length(min=8, max=100),
        Optional("status"): In([member.value for member in StatusEnum]),
    },
)

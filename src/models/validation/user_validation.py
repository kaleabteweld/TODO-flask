from voluptuous import Schema, Length, Email

user_validation_schema = Schema(
    {
        "username": Length(min=8, max=50),
        "email": Email(Length(min=8, max=50)),
        "password": Length(min=8, max=50),
    },
    required=True,
)

user_login_validation_schema = Schema(
    {"email": Length(min=8, max=50), "password": Length(min=8, max=50)},
    required=True,
)

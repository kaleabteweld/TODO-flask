from enum import Enum


class Pagination:
    def __init__(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset

    def to_dict(self):
        return {
            "limit": self.limit,
            "offset": self.offset,
        }


class StatusEnum(str, Enum):
    onGoing = "onGoing"
    abort = "abort"
    completed = "completed"

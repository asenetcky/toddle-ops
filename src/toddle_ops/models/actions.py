from pydantic import BaseModel


from toddle_ops.enums import Status


# # TODO add description annotations etc...
class ActionReport(BaseModel):
    status: Status
    message: str | None

from pydantic import BaseModel, Field

from toddle_ops.enums import Status
from toddle_ops.models.projects import StandardProject


# Model representing a status report
# Typically used for signaling status in workflows
class StatusReport(BaseModel):
    status: Status = Field(description="The status of the report.")
    message: str | None = Field(
        None,
        description="Optional message providing additional information about the status.",
    )
    project: StandardProject | None = Field(
        None,
        description="Optional project if applicable.",
    )

from toddle_ops.enums import Status
from toddle_ops.models.reports import StatusReport


# helper function for exiting loops
def exit_loop():
    """
    Helpers to create a StatusReport indicating loop exit.
    Returns:
        StatusReport: A report with status APPROVED to signal loop exit.
    """
    return StatusReport(status=Status.APPROVED, message="Approved. Exiting loop.")

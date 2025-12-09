def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the
    project quality assurance process is finished and no more changes are

    needed."""
    return {
        "status": "approved",
        "message": "Project approved. Exiting Quality Assurance loop.",
    }


# TODO implement exit loop with status and/or action report

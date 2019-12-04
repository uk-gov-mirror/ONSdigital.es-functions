class NoDataInQueueError(Exception):
    """
    Custom exception signifying that there is no data in the queue
    (the response did not contain messages)
    """

    pass


class MethodFailure(Exception):
    """
    Custom exception signifying that the method has encountered an exception.
    """
    def __init__(self, message):
        self.error_message = message

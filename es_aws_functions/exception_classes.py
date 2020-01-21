class DoNotHaveAllDataError(Exception):
    """
    Custom exception used by the modules which need to take more than
    one message from a queue, but fail to.
    """
    pass


class LambdaFailure(Exception):
    """
    Custom exception signifying that the lambda has failed.
    This is to be passed back to the step function.
    """
    def __init__(self, message):
        self.error_message = message


class MethodFailure(Exception):
    """
    Custom exception signifying that the method has encountered an exception.
    """
    def __init__(self, message):
        self.error_message = message


class NoDataInQueueError(Exception):
    """
    Custom exception signifying that there is no data in the queue
    (the response did not contain messages)
    """

    pass

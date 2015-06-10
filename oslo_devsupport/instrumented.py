
import datetime

from .model import entrypoint
from .model import stack
from . import context

class Instrumented(object):

    def __init__(self, operation, toplevel=False):
        self.operation = operation
        self.toplevel = toplevel

    def __enter__(self):
        self.operation.start = datetime.datetime.utcnow()

        if self.toplevel:
            context.start(self.operation)
        else:
            context.push(self.operation)

        return self

    def __exit__(self, type, value, tb):
        self.finish = datetime.datetime.utcnow()
        if type:
            self.exception = stack.ExceptionTrace.from_traceback(type, value, tb)

        if self.toplevel:
            context.finish(self.operation)
        else:
            context.pop(self.operation)


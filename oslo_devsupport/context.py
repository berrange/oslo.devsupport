
import threading

from oslo_log import log as logging

LOG = logging.getLogger(__name__)

class Context(object):

    def __init__(self):
        super(Context, self).__init__()
        self.stack = threading.local()
        self.consumer = None

    def start(self, operation):
        LOG.error("Start %s %s" % (self.consumer, operation))
        if self.consumer is None:
            return

        stack = getattr(self.stack, "stack", None)
        if stack is not None:
            raise Exception("Operation already running")
        self.stack.stack = [operation]

    def push(self, operation):
        stack = getattr(self.stack, "stack", None)
        if stack is None:
            LOG.debug("Discarding orphaned operation %s" % operation)
            return

        stack[-1].children.append(operation)
        stack.append(operation)


    def finish(self, operation):
        stack = getattr(self.stack, "stack", None)
        if stack is None:
            return
        if stack[0] != operation:
            return

        self.stack.stack = None

        LOG.error("Finish %s: %s" % (self.consumer, operation))
        if self.consumer is None:
            return

        try:
            self.consumer.process(operation)
        except Exception as e:
            # Never allow developer support to actually
            # break operation of the system
            LOG.error("Failed to save operation: %s" % str(e))

    def pop(self, operation):
        stack = getattr(self.stack, "stack", None)
        if stack is None:
            return
        if stack[-1] == operation:
            stack.pop()


_CONTEXT = Context()

def dispatch(consumer):
    LOG.error("Dispatch %s %s" % (_CONTEXT, consumer))
    _CONTEXT.consumer = consumer

def push(operation):
    _CONTEXT.push(operation)

def pop(operation):
    _CONTEXT.pop(operation)

def start(operation):
    _CONTEXT.start(operation)

def finish(operation):
    _CONTEXT.finish(operation)

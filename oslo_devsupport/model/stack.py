

import inspect
import traceback

from oslo_versionedobjects import base
from oslo_versionedobjects import fields

@base.VersionedObjectRegistry.register
class StackFrame(base.VersionedObject):

    # Version 1.0: Initial version
    VERSION = "1.0"

    OBJ_PROJECT_NAMESPACE = "devsupport"

    fields = {
        'filename': fields.StringField(),
        'lineno': fields.IntegerField(),
        'function': fields.StringField(),
    }


class StackBase(base.VersionedObject):

    # Version 1.0: Initial version
    VERSION = "1.0"

    OBJ_PROJECT_NAMESPACE = "devsupport"

    fields = {
        'frames': fields.ListOfObjectsField("StackFrame"),
    }

    obj_relationships = {
        'frames': [('1.0', '1.0')],
    }


@base.VersionedObjectRegistry.register
class StackTrace(StackBase):

    # Version 1.0: Initial version
    VERSION = "1.0"

    @classmethod
    def from_stack(cls, stack):
        frames = [
            StackFrame(filename=frame[1],
                       lineno=frame[2],
                       function=frame[3])
            for frame in stack
        ]
        return cls(frames=frames)

    @classmethod
    def from_caller(cls, skip=1):
        stack = inspect.stack()
        return cls.from_stack(stack[skip:])


@base.VersionedObjectRegistry.register
class ExceptionTrace(StackBase):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'typename': fields.StringField(),
        'message': fields.StringField(),
    }

    @classmethod
    def from_traceback(cls, type, value, tb):
        frames = [
            StackFrame(filename=frame[0],
                       lineno=frame[1],
                       function=frame[2])
            for frame in traceback.extract_tb(tb)
        ]
        return cls(typename=type.__name__,
                   message=str(value),
                   frames=frames)

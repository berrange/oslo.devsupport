
from . import operation

from oslo_versionedobjects import fields
from oslo_versionedobjects import base

@base.VersionedObjectRegistry.register
class MethodCall(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'module': fields.StringField(),
        'method': fields.StringField(),
        'args': fields.ListOfStringsField(),
        'kwargs': fields.DictOfStringsField(),
    }

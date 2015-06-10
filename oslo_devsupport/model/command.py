
from . import operation

from oslo_versionedobjects import fields
from oslo_versionedobjects import base

@base.VersionedObjectRegistry.register
class CommandExecute(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'command': fields.StringField(),
        'params': fields.ListOfStringsField(nullable=True),
        'environ': fields.DictOfStringsField(nullable=True),
        'cwd': fields.StringField(nullable=True),
        'shell': fields.BooleanField(nullable=True)
    }

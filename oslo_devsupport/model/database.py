
from . import operation

from oslo_versionedobjects import fields
from oslo_versionedobjects import base

@base.VersionedObjectRegistry.register
class DatabaseRequest(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'sql': fields.StringField(),
        'params': fields.ListOfStringsField(),
    }

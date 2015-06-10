
from . import operation

from oslo_versionedobjects import fields
from oslo_versionedobjects import base

@base.VersionedObjectRegistry.register
class Group(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'label': fields.StringField()
    }

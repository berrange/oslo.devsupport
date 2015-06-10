

from . import operation

from oslo_versionedobjects import base
from oslo_versionedobjects import fields

class ThreadBase(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'module': fields.StringField(),
        'method': fields.StringField(),
        'args': fields.ListOfStringsField(),
        'kwargs': fields.DictOfStringsField(),
    }


@base.VersionedObjectRegistry.register
class ThreadSpawn(ThreadBase):
    pass


@base.VersionedObjectRegistry.register
class ThreadExecute(ThreadBase):
    pass


from . import operation

from oslo_versionedobjects import fields
from oslo_versionedobjects import base

class MessagingBase(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'server': fields.StringField(nullable=True),
        'topic': fields.StringField(),
        'namespace': fields.StringField(nullable=True),
        'version': fields.StringField(),
        'method': fields.StringField(),
        'params': fields.DictOfStringsField(),
    }


@base.VersionedObjectRegistry.register
class MessagingCast(MessagingBase):
    pass


@base.VersionedObjectRegistry.register
class MessagingCall(MessagingBase):
    pass


@base.VersionedObjectRegistry.register
class MessagingDispatch(MessagingBase):
    pass

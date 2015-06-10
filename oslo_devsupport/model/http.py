
from . import operation

from oslo_versionedobjects import fields
from oslo_versionedobjects import base

class HTTPMethod(fields.Enum):

    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    TRACE = "TRACE"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    PATCH = "PATCH"

    ALL = [
        GET, HEAD, POST, PUT, DELETE,
        TRACE, OPTIONS, CONNECT, PATCH
    ]

    def __init__(self):
        super(HTTPMethod, self).__init__(valid_values=HTTPMethod.ALL)


class HTTPMethodField(fields.BaseEnumField):

    AUTO_TYPE = HTTPMethod()


class HTTPBase(operation.Operation):

    # Version 1.0: Initial version
    VERSION = "1.0"

    fields = {
        'method': HTTPMethodField(),
        'url': fields.StringField(),
        'params': fields.DictOfStringsField(),
        'headers': fields.DictOfStringsField(),
    }


@base.VersionedObjectRegistry.register
class HTTPRequest(HTTPBase):
    pass


@base.VersionedObjectRegistry.register
class HTTPDispatch(HTTPBase):
    pass

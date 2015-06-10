
from . import stack

from oslo_versionedobjects import base
from oslo_versionedobjects import fields


class SubObject(fields.FieldType):
    def __init__(self, obj_names, **kwargs):
        self._obj_names = obj_names
        super(SubObject, self).__init__(**kwargs)

    def coerce(self, obj, attr, value):
        try:
            obj_name = value.obj_name()
        except AttributeError:
            obj_name = ""

        if obj_name not in self._obj_names:
            raise ValueError(_('An object of type %(types)s is required '
                               'in field %(attr)s') %
                             {'type': ",".join(self._obj_names), 'attr': attr})
        return value

    @staticmethod
    def to_primitive(obj, attr, value):
        return value.obj_to_primitive()

    @staticmethod
    def from_primitive(obj, attr, value):
        # FIXME(danms): Avoid circular import from base.py
        from oslo_versionedobjects import base as obj_base
        # NOTE (ndipanov): If they already got hydrated by the serializer, just
        # pass them back unchanged
        if isinstance(value, obj_base.VersionedObject):
            return value
        return obj_base.VersionedObject.obj_from_primitive(value, obj._context)

    def describe(self):
        return "Object<%s>" % ",".join(self._obj_names)

    def stringify(self, value):
        if 'uuid' in value.fields:
            ident = '(%s)' % (value.obj_attr_is_set('uuid') and value.uuid or
                              'UNKNOWN')
        elif 'id' in value.fields:
            ident = '(%s)' % (value.obj_attr_is_set('id') and value.id or
                              'UNKNOWN')
        else:
            ident = ''

        return '%s%s' % (",".join(self._obj_names), ident)


# This inheritance is a hack so the annoying isinstance check
# in obj_reset_changes() processes our custom field :-(
# Really the Field class should have a obj_reset_changes
# method so VersionedObject doesn't have to hardcode this
# list of types
class ListOfSubObjectsField(fields.ListOfObjectsField):
    def __init__(self, objtypes, **kwargs):
        self.AUTO_TYPE = fields.List(SubObject(objtypes))
        super(ListOfSubObjectsField, self).__init__(objtypes[0], **kwargs)


class Operation(base.VersionedObject):

    # Version 1.0: Initial version
    VERSION = "1.0"

    OBJ_PROJECT_NAMESPACE = "devsupport"

    fields = {
        'start': fields.DateTimeField(nullable=True),
        'finish': fields.DateTimeField(nullable=True),

        'callstack': fields.ObjectField('StackTrace',
                                        nullable=True),

        'exception': fields.ObjectField('ExceptionTrace'),

        'children': ListOfSubObjectsField(
            ['CommandExecute',
             'DatabaseRequest',
             'EntryPoint',
             'Group',
             'HTTPRequest',
             'HTTPDispatch',
             'MessagingCall',
             'MessagingCast',
             'MessagingDispatch',
             'MethodCall',
             'ThreadSpawn',
             'ThreadExecute'],
            nullable=True)
    }

    obj_relationships = {
        'callstack': [('1.0', '1.0')],
        'exception': [('1.0', '1.0')],
        'children': [('1.0', '1.0')],
    }

    def obj_load_attr(self, attrname):
        if attrname == "children":
            self.children = []
            return

        super(Operation, self).obj_load_attr(attrname)

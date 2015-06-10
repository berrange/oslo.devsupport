
import sys
import uuid

from oslo_utils import importutils
from oslo_log import log as logging

from . import context
from . import instrumented
from . import consumer
from . import options
from . import model

LOG = logging.getLogger(__name__)

_CALLSTACK = False

def _load_consumer_nop(conf, service_Name):
    return consumer.NoOpConsumer()

def _load_consumer_file(conf, service_name):
    return consumer.FileConsumer(
        conf.devsupport.enabled,
        service_name,
        conf.devsupport.data_dir)

def _load_consumer(conf, service_name):
    name = "_load_consumer_" + conf.devsupport.consumer
    method = getattr(sys.modules[__name__], name)
    return method(conf, service_name)

def setup(conf, service_name):
    options.register(conf)

    # oslo_devsupport.model uses olso_versionedobjects
    # oslo_versionedobjects depends on olso_messaging
    # oslo_messaging uses oslo_devsupport
    #
    # So if we imported the model by defualt we'd cause
    # a painful circular dependancy at import time. Thus
    # we only import the model when we setup devsupport
    #global model
    #model = importutils.import_module("oslo_devsupport.model")
    consumer = _load_consumer(conf, service_name)
    LOG.info("Loaded consumer %(consumer)s enabled=%(enabled)s" %
             {"consumer": consumer, "enabled": consumer.enabled})
    context.dispatch(consumer)

    global _CALLSTACK
    _CALLSTACK = conf.devsupport.callstack


def _flatten(orig):
    if orig is None:
        return None

    if type(orig) in (list, tuple):
        return [
            str(item) for item in orig
        ]
    elif type(orig) == dict:
        new = {}
        for key in orig.keys():
            new[key] = str(orig[key])
        return new
    else:
        return str(orig)


class MockModel(object):

    def __setattr__(self, name, value):
        pass

    def __getattr__(self, name):
        pass

def _callstack():
    global _CALLSTACK
    if not _CALLSTACK:
        return None

    # 2 - strip of this method, and the one above
    return model.StackTrace.from_caller(2)


def command_execute(command, params, environ, cwd, shell):
    return instrumented.Instrumented(
        model.CommandExecute(
            callstack=_callstack(),
            command=command,
            params=_flatten(params),
            environ=_flatten(environ),
            cwd=cwd,
            shell=shell))

def database_request(sql, params):
    return instrumented.Instrumented(
        model.DatabaseRequest(
            callstack=_callstack(),
            sql=sql,
            params=_flatten(params)))

def entry_point(id=None):
    if id is None:
        id = str(uuid.uuid4())
    return instrumented.Instrumented(
        model.EntryPoint(
            callstack=_callstack(),
            uuid=id),
        toplevel=True)

def group(label):
    return instrumented.Instrumented(
        model.Group(
            callstack=_callstack(),
            label=label))

def http_request(method, url, params, headers):
    return instrumented.Instrumented(
        model.HTTPRequest(
            callstack=_callstack(),
            method=method,
            url=url,
            params=_flatten(params),
            headers=_flatten(headers)))

def http_dispatch(method, url, params, headers):
    return instrumented.Instrumented(
        model.HTTPDispatch(
            callstack=_callstack(),
            method=method,
            url=url,
            params=_flatten(params),
            headers=_flatten(headers)))

def messaging_cast(server, topic, namespace, version, method, params):
    return instrumented.Instrumented(
        model.MessagingCast(
            callstack=_callstack(),
            server=server,
            topic=topic,
            namespace=namespace,
            version=version,
            method=method,
            params=_flatten(params)))

def messaging_call(server, topic, namespace, version, method, params):
    return instrumented.Instrumented(
        model.MessagingCall(
            callstack=_callstack(),
            server=server,
            topic=topic,
            namespace=namespace,
            version=version,
            method=method,
            params=_flatten(params)))


def messaging_dispatch(server, topic, namespace, version, method, params):
    return instrumented.Instrumented(
        model.MessagingDispatch(
            callstack=_callstack(),
            server=server,
            topic=topic,
            namespace=namespace,
            version=version,
            method=method,
            params=_flatten(params)))


def method_call(module, method, params):
    return instrumented.Instrumented(
        model.MethodCall(
            callstack=_callstack(),
            module=module,
            method=method,
            params=_flatten(params)))

def thread_spawn(module, method, args, kwargs):
    LOG.error("module=%s method=%s args=%s kwargs=%s",
              module, method, args, kwargs)
    return instrumented.Instrumented(
        model.ThreadSpawn(
            callstack=_callstack(),
            module=module,
            method=method,
            args=_flatten(args),
            kwargs=_flatten(kwargs)))


def thread_execute(module, method, args, kwargs):
    return instrumented.Instrumented(
        model.ThreadExecute(
            callstack=_callstack(),
            module=module,
            method=method,
            args=_flatten(args),
            kwargs=_flatten(kwargs)))

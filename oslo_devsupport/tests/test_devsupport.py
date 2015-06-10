

import testtools
import logging

from oslo_config import cfg

import oslo_devsupport as ods
from oslo_devsupport import model
from oslo_devsupport import consumer
from oslo_devsupport import context


class MemoryConsumer(consumer.Consumer):

    def __init__(self):

        self.operations = []

    def _process(self, operation):
        self.operations.append(operation)

class DevSupportTestCase(testtools.TestCase):

    def setUp(self):
        super(DevSupportTestCase, self).setUp()

        logging.basicConfig(level=logging.DEBUG)
        ods.setup(cfg.CONF, "test-service")

    def test_context(self):
        import sys
        global model
        global consumer
        print >>sys.stderr, "%s" % model
        print >>sys.stderr, "%s" % consumer
        consumer = MemoryConsumer()
        consumer.enable()
        context.dispatch(consumer)
        with ods.entry_point("22616ce3-6c37-49e8-be2d-a98a52045482") as req:
            with ods.http_request("GET",
                                 "/foo/bar",
                                 {"foo": "bzar"},
                                 {"wizz": "ooh"}):
                with ods.method_call("libvirt.virConnect",
                                    "open",
                                    "qemu:///system"):
                    pass
                with ods.method_call("libvirt.virDomain",
                                    "shutdown",
                                    "virDomainPtr"):
                    pass
                with ods.database_request("update foo set wwk='?' where foo='?'",
                                          ["eeek", "barr"]):
                    pass
                with ods.messaging_call("foo.example.com", "compute",
                                        "nova", "1.0", "start", {"foo": "bar"}):
                    pass
                try:
                    with ods.method_call("libvirt.virDomain",
                                        "destroy",
                                        "virDomainptr"):
                        raise Exception("Failed")
                except:
                    pass

        expect = model.EntryPoint(
            uuid="22616ce3-6c37-49e8-be2d-a98a52045482",
            children=[
                model.HTTPRequest(
                    method="GET",
                    url="/foo/bar",
                    params={"foo": "bar"},
                    headers={"wizz": "ooh"})
            ])

        self.assertEqual(1, len(consumer.operations))
        print >>sys.stderr, "%s" % expect
        self.assertEqual(expect, consumer.operations[0])


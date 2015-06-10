
import argparse
import logging
import json
import os
import os.path
import sys

import oslo_devsupport as ods
from oslo_devsupport import model


def summarize_node(node, starttime=None, depth=0):
    if starttime is None:
        starttime = node.start
    duration = node.finish - node.start
    delta = node.start - starttime

    indent = "  " * depth
    print "+%2.02fs %-2.02fs %s%s" % (delta, duration, indent, node)

    for child in node.children:
        summarize_node(child, starttime, depth+1)

def summarize_file(filename):
    with open(filename, "r") as fh:
        data = fh.read()
        objdata = json.loads(data)
        node = model.EntryPoint.obj_from_primitive(objdata)
        summarize_node(node)

def get_data_files(datadir, hostnames, services):
    for hostname in os.listdir(datadir):
        if len(hostnames) == 0 or hostname in hostnames:
            hostdir = os.path.join(datadir, hostname)
            for service in os.listdir(hostdir):
                servicedir = os.path.join(hostdir, service)
                if len(services) == 0 or service in services:
                    for datafile in os.listdir(servicedir):
                        yield os.path.join(servicedir, datafile)


class Command(object):

    def register(self, parser):
        pass

    def run(self, args):
        pass

class SummaryCommand(Command):

    def register(self, subparser):
        parser = subparser.add_parser("summary",
                                      help="Summarize report timings")
        parser.set_defaults(func=self.run)

    def run(self, args):
        for filename in get_data_files(args.datadir,
                                       args.hostnames,
                                       args.services):
            print
            print ">>> " + filename + " <<<"
            print
            summarize_file(filename)


class Report(object):

    def run(self):
        parser = argparse.ArgumentParser(description="Oslo Developer Support")
        parser.add_argument("--datadir", default="/var/spool/oslo-devsupport",
                            dest="datadir",
                            help="Report data directory")
        parser.add_argument("--hostname", default=[],
                            dest="hostnames", action="append",
                            help="OpenStack host name")
        parser.add_argument("--service", default=[],
                            dest="services", action="append",
                            help="OpenStack service name")

        subparser = parser.add_subparsers(help="Commands")
        summary = SummaryCommand()
        summary.register(subparser)

        args = parser.parse_args()

        args.func(args)
        return 0


def main():
    logging.basicConfig(level=logging.DEBUG)
    report = Report()

    try:
        sys.exit(report.run())
    except Exception, e:
        print >>sys.stderr, "%s: %s" % (sys.argv[0], str(e))
        raise
        sys.exit(1)

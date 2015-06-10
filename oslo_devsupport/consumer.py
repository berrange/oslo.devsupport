
import json
import os.path
import socket

class Consumer(object):

    def __init__(self, enabled):
        self.enabled = enabled

    def _process(self, operation):
        raise NotImplementedError()

    def process(self, operation):
        if self.enabled:
            self._process(operation)

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


class NoOpConsumer(Consumer):

    def _process(self, operation):
        pass


class FileConsumer(Consumer):

    def __init__(self, enabled, appname, directory):
        super(FileConsumer, self).__init__(enabled)

        self.directory = directory
        self.appname = appname

    def _process(self, operation):

        dirname = os.path.join(self.directory, socket.gethostname(), self.appname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        filename = os.path.join(dirname, operation.uuid + ".json")

        operation.obj_reset_changes(recursive=True)
        try:
            with open(filename, "w") as fh:
                print >>fh, json.dumps(operation.obj_to_primitive(), indent=4)
        except Exception as e:
            try:
                os.unlink(filename)
            except:
                pass
            raise e

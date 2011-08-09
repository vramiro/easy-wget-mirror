import re, os, errno
from MirrorPlugin import MirrorPlugin

class CreateDirectoriesException(Exception): pass

class CreateDirectories(MirrorPlugin):

    def __init__(self, *args, **kwargs):
        try:
            m = kwargs['mirror']
            super(CreateDirectories, self).__init__(m)
            self.destination_path = self.mirror.destination
            self.logs_path = self.mirror.logs_path

        except Exception as e:
            raise CreateDirectoriesException("Unable to init CreateDirectories plugin: " + str(e))

    def __before__(self, buff):
        self.create_dir(self.destination_path)
        self.create_dir(self.logs_path)
    
    def __after__(self, buff):
        pass

    def create_dir(self, path):
        p = os.path.abspath(path)
        try:
            os.makedirs(p)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise    


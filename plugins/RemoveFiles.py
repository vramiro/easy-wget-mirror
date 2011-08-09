import re, os
from MirrorPlugin import MirrorPlugin

class RemoveFilesException(Exception): pass

class RemoveFiles(MirrorPlugin):

    def __init__(self, *args, **kwargs):
        try:
            m = kwargs['mirror']
            config = kwargs['config']
            super(RemoveFiles, self).__init__(m)
            self.destination = self.mirror.destination
            self.patterns = [s[1:-1] for s in config.get(RemoveFiles.__name__,'patterns').split(',')]

        except Exception as e:
            raise RemoveFilesException("Unable to init RemoveFiles plugin: " + str(e))

    def __before__(self, buff):
        pass
    
    def __after__(self, buff):
        for d in os.listdir(self.destination):
            path = os.path.join(self.destination, d)
            for pattern in self.patterns:
                if re.match(pattern, d): os.rmdir(path)


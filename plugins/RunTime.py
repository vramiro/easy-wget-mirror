import os
from MirrorPlugin import MirrorPlugin

class RunTimeException(Exception): pass

class RunTime(MirrorPlugin):

    def __init__(self, *args, **kwargs):
        try:
            m = kwargs['mirror']
            super(RunTime, self).__init__(m)

        except Exception as e:
            raise RunTimeException("Unable to init RunTime plugin: " + str(e))

    def __before__(self, buff):        
        self.init = os.times()[4]
    
    def __after__(self, buff):
        self.end = os.times()[4]
        rtime = self.end - self.init
        buff.write('Exec Time:\t%s secs\n' % (str(rtime)))

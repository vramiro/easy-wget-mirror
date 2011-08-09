import os
from MirrorPlugin import MirrorPlugin

class RunDateException(Exception): pass

class RunDate(MirrorPlugin):

    def __init__(self, *args, **kwargs):
        try:
            m = kwargs['mirror']
            super(RunDate, self).__init__(m)

        except Exception as e:
            raise RunDateException("Unable to init RunDate plugin: " + str(e))

    def __before__(self, buff):
        buff.write('Run Date:\t%s\n' % self.mirror.run_date.strftime('%Y/%m/%d'))
    
    def __after__(self, buff):
        pass

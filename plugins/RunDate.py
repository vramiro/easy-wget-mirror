import os
from MirrorPlugin import MirrorPlugin

DEFAULT_FORMAT='%Y/%m/%d %H:%M:%S'

class RunDateException(Exception): pass

class RunDate(MirrorPlugin):

    def __init__(self, *args, **kwargs):
        try:
            m = kwargs['mirror']
            super(RunDate, self).__init__(m)

            config = kwargs['config']

            if config.has_option(RunDate.__name__,'format'):
                self.format = config.get(RunDate.__name__,'format')        
            else:
                self.format = DEFAULT_FORMAT


        except Exception as e:
            raise RunDateException("Unable to init RunDate plugin: " + str(e))

    def __before__(self, buff):
        buff.write('Run Date:\t%s\n' %
                   self.mirror.run_date.strftime(self.format))
    
    def __after__(self, buff):
        pass

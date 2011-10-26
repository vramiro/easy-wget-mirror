import os
from pwd import getpwnam
from grp import getgrnam
from MirrorPlugin import MirrorPlugin

class ChangeOwnerException(Exception): pass

class ChangeOwner(MirrorPlugin):

    def __init__(self, *args, **kwargs):
        try:
            m = kwargs['mirror']
            config = kwargs['config']

            super(ChangeOwner, self).__init__(m)

            self.destination = self.mirror.destination

            username = config.get(ChangeOwner.__name__,'user')        
            user = getpwnam(username)
            self.uid = user.pw_uid

            groupname = config.get(ChangeOwner.__name__,'group')
            group = getgrnam(groupname)            
            self.gid = group.gr_gid
            
        except Exception as e:
            raise ChangeOwnerException("Unable to init ChangeOwner plugin: " + str(e))

    def __before__(self, buff):
        pass
    
    def __after__(self, buff):
        for root, dirs, files in os.walk(self.destination):
            os.chown(root, self.uid, self.gid)
            for momo in dirs:
                os.chown(os.path.join(root, momo), self.uid, self.gid)
            for momo in files:
                os.chown(os.path.join(root, momo), self.uid, self.gid)
        


class MirrorPlugin(object):
    def __init__(self, mirror, *args, **kwargs): self.mirror = mirror
    def __before__(self, buff): raise SubClassResponsability
    def __after__(self, buff): raise SubClassResponsability

class SubClassResponsability(Exception): pass

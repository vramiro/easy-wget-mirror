class MirrorPlugin(object):
    def __init__(self, mirror): self.mirror = mirror
    def __before__(self, buff):
        raise SubClassResponsability("Should be implemented by subclass")
    def __after__(self, buff):
        raise SubClassResponsability("Should be implemented by subclass")

class SubClassResponsability(Exception): pass

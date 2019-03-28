class Data():
    def __init__(self, action="clear", *args, force=False, loop=False):
        self.args = args
        self.action = action
        self.force = force
        self.loop = loop
        pass

__author__ = 'Janek Krukowski'


class Process(object):
    def __init__(self, algo):
        self.algo = algo


class ProcessManager(object):
    def __init__(self, nmax=10, frames=40):
        self.nmax = nmax
        self.frames = frames

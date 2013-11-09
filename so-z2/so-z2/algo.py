__author__ = 'Janek Krukowski'
import random
from itertools import izip

random.seed()

class Hd(object):

    def __init__(self, nmax):
        self.nmax = nmax
        self._data = [i for i in xrange(self.nmax)]
        self._start = random.randint(0, self.nmax)

    @property
    def data(self):
        return self._data

    @property
    def start(self):
        return self._start

    @property
    def capacity(self):
        return self.nmax

class Demand(object):

    def __init__(self, hd, count):
        self.hd = hd
        self.count = count
        self._data = [random.choice(self.hd.data) for i in xrange(self.count)]

    @property
    def data(self):
        return self._data

# FCFS, SSTF, SCAN i C-SCAN

class Algo(object):

    def __init__(self, hd, demand):
        self.hd = hd
        self.demand = demand
        self._score = []
        self.first = hd.start

    def process(self):
        raise NotImplementedError()

    def move(self, start, to):
        self._score.append(abs(start - to))

    @property
    def score(self):
        return sum(self._score)

class Fcfs(Algo):

    def __init__(self, hd, demand):
        super(Fcfs, self).__init__(hd, demand)

    def process(self):
        self.move(self.first, self.demand.data[0])
        for i, j in izip(self.demand.data[0::2], self.demand.data[1::2]):
            self.move(i, j)


class Ssft(Algo):

    def __init__(self, hd, demand):
        super(Ssft, self).__init__(hd, demand)

class Scan(Algo):

    def __init__(self, hd, demand):
        super(Scan, self).__init__(hd, demand)

class Cscan(Algo):

    def __init__(self, hd, demand):
        super(Cscan, self).__init__(hd, demand)


if __name__ == '__main__':
    hd = Hd(100)
    demand = Demand(hd, 10)
    print demand.data, hd.start
    fcfs = Fcfs(hd, demand)
    fcfs.process()
    print fcfs.score




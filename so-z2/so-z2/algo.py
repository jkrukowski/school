__author__ = 'Janek Krukowski'
import random
from itertools import izip, tee, chain

random.seed()


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


class Proc(object):
    """Represents single IO item"""

    def __init__(self, proc_no, deadline):
        self.proc_no = proc_no
        self.deadline = deadline

    @classmethod
    def from_random(cls, max_proc, max_deadline):
        return cls(random.randint(0, max_proc), random.randint(0, max_deadline))

    def __repr__(self):
        return "<PROC: n: {0}, d: {1}>".format(self.proc_no, self.deadline)


class Hd(object):
    """Represents disk"""

    def __init__(self, nmax, arg_start=None):
        self.nmax = nmax
        self._data = [i for i in xrange(self.nmax)]
        self._start = arg_start
        if not arg_start:
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
    """Represents demand"""
    def __init__(self, hd, count, arg_data=None):
        self.hd = hd
        self.count = count
        self._data = arg_data
        if not arg_data:
            self._data = [random.choice(self.hd.data) for i in xrange(self.count)]

    @property
    def data(self):
        return self._data


class Algo(object):
    """Base class for all scheduling algorithms"""
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
        for i, j in pairwise(self.demand.data):
            self.move(i, j)


class Ssft(Algo):
    def __init__(self, hd, demand):
        super(Ssft, self).__init__(hd, demand)

    def get_closest(self, iterable, item):
        return min(iterable, key=lambda x: abs(x - item))

    def process(self):
        closest = self.get_closest(self.demand.data, self.first)
        self.move(self.first, closest)
        self.demand.data.remove(closest)
        while self.demand.data:
            item = self.get_closest(self.demand.data, closest)
            self.move(closest, item)
            self.demand.data.remove(item)
            closest = item


class Scan(Algo):
    def __init__(self, hd, demand):
        super(Scan, self).__init__(hd, demand)

    def process(self):
        lower = sorted([i for i in self.demand.data if i < self.first], reverse=True)
        lower.append(0)
        lower.extend(sorted([i for i in self.demand.data if i >= self.first]))
        self.move(self.first, lower[0])
        for i, j in pairwise(lower):
            self.move(i, j)


class Cscan(Algo):
    def __init__(self, hd, demand):
        super(Cscan, self).__init__(hd, demand)

    def process(self):
        higher = sorted([i for i in self.demand.data if i >= self.first])
        higher.extend([hd.capacity - 1, 0])
        higher.extend(sorted([i for i in self.demand.data if i < self.first]))
        self.move(self.first, higher[0])
        for i, j in pairwise(higher):
            self.move(i, j)


if __name__ == '__main__':
    hd = Hd(200, arg_start=65)
    demand = Demand(hd, 10, arg_data=[100, 198, 44, 132, 2, 134, 70, 72])
    print demand.data, hd.start
    algo = Cscan(hd, demand)
    algo.process()
    print algo.score
    print Proc.from_random(10, 3)




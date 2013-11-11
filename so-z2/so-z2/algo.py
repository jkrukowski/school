__author__ = 'Janek Krukowski'
import random
from itertools import izip, tee, chain

random.seed()
MAX_DEADLINE = 3


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


class Proc(object):
    """Represents single IO item"""

    def __init__(self, no, deadline=None, real_prob=0.3):
        self.no = no
        self.deadline = deadline
        self._is_real = random.random() < real_prob
        if self.deadline is None:
            self.deadline = random.randint(0, MAX_DEADLINE)

    @classmethod
    def from_random(cls, max_no):
        return cls(random.randint(0, max_no))

    @property
    def is_real(self):
        return self._is_real

    def __sub__(self, other):
        return Proc(self.no - other.no, self.deadline)

    def __abs__(self):
        return Proc(abs(self.no), self.deadline)

    def __cmp__(self, other):
        return cmp(self.no, other.no)

    def __repr__(self):
        return "<PROC: n: {0}, d: {1}, {2}>".format(self.no, self.deadline, self._is_real)


class Hd(object):
    """Represents disk"""

    def __init__(self, nmax, arg_start=None):
        self.nmax = nmax
        self._data = [i for i in xrange(self.nmax)]
        self._start = Proc(arg_start)
        if not arg_start:
            self._start = Proc.from_random(self.nmax)

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
    """Represents single demand"""

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
        self._score.append(abs(start - to).no)

    @property
    def score(self):
        return sum(self._score)


class RealTime(object):
    """Base class for realtime algorithms"""

    def __init__(self, algo, hd, demand):
        self.hd = hd
        self.demand = demand
        self.algo = algo
        self._score = []
        self.first = hd.start

    def move(self, start, to):
        self._score.append(abs(start - to).no)

    @property
    def score(self):
        return sum(self._score)

    def process(self):
        raise NotImplementedError()


class Edf(RealTime):
    def __init__(self, algo, hd, demand):
        super(Edf, self).__init__(algo, hd, demand)

    def process(self):
        # real processes
        real_proc = sorted([i for i in self.demand.data if i.is_real], key=lambda x: x.deadline)
        if real_proc:
            self.move(self.first, real_proc[0])
            for i, j in pairwise(real_proc):
                self.move(i, j)

        # normal processes
        normal_proc = [i for i in self.demand.data if not i.is_real]
        if normal_proc:
            algo = self.algo(self.hd, Demand(hd=self.hd, count=len(normal_proc), arg_data=normal_proc))
            algo.first = real_proc[-1]
            algo.process()
            self._score.extend(algo._score)

class Fdscan(RealTime):
    def __init__(self, algo, hd, demand):
        super(Fdscan, self).__init__(algo, hd, demand)

    def get_closest(self, iterable):
        item = min(iterable, key=lambda x: x.deadline)
        return iterable.index(item)

    def process(self):
        start = 0
        self.move(self.first, self.demand.data[0])
        real_proc = sorted([i for i in self.demand.data if i.is_real], key=lambda x: x.deadline)
        for i in real_proc:
            idx = self.demand.data.index(i)
            for i, j in pairwise(self.demand.data[start:idx+1]):
                self.move(i, j)



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
        higher.extend([Proc(hd.capacity - 1), Proc(0)])
        higher.extend(sorted([i for i in self.demand.data if i < self.first]))
        self.move(self.first, higher[0])
        for i, j in pairwise(higher):
            self.move(i, j)


if __name__ == '__main__':
    hd = Hd(200, arg_start=65)
    data = [Proc(100), Proc(198), Proc(44), Proc(132), Proc(2), Proc(134), Proc(70), Proc(72)]
    demand = Demand(hd, count=10, arg_data=data)
    print demand.data, hd.start
    algo = Fdscan(Fcfs, hd, demand)
    algo.process()
    print algo.score




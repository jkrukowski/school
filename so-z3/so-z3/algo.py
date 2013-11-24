__author__ = 'Janek Krukowski'

from collections import namedtuple
import random

random.seed()
Frame = namedtuple('Frame', 'number')


def get_calls(*args):
    return [Frame(number=i) for i in args]


def get_random_calls(nmax, count=1000):
    return [Frame(number=random.randint(0, nmax)) for i in xrange(count)]


class Algo(object):
    """Base class for algorithms"""

    def __init__(self, count):
        self.swaps = 0
        self.last_swapped = 0
        self.count = count
        self.data = {i: None for i in xrange(count)}

    def find_key(self, frame, **kwargs):
        for k, v in self.data.iteritems():
            if not v:
                self.swaps += 1
                return k
        return self.swap(frame, **kwargs)

    def exists(self, frame):
        return frame in set(self.data.values())

    def put(self, frame, **kwargs):
        if not self.exists(frame):
            key = self.find_key(frame, **kwargs)
            self.data[key] = frame

    def swap(self, frame, **kwargs):
        raise NotImplementedError()


class Fifo(Algo):
    def swap(self, frame, **kwargs):
        self.swaps += 1
        result = self.last_swapped
        self.last_swapped += 1
        self.last_swapped %= len(self.data)
        return result


class Opt(Algo):
    def swap(self, frame, **kwargs):
        self.swaps += 1
        tail = kwargs['tail']
        index = []
        for i in self.data.values():
            try:
                index.append(tail.index(i))
            except ValueError:
                index.append(-1)
        result = sorted(zip(self.data.values(), index), key=lambda x: x[1], reverse=True)
        return result[0][1]


class Lru(Algo):
    def __init__(self, count):
        super(Lru, self).__init__(count)
        self.buff = [None for i in xrange(count)]

    def fill_buff(self, frame):
        try:
            self.buff.remove(frame)
        except ValueError:
            self.buff.pop(0)
        self.buff.append(frame)

    def last_used(self):
        last = self.buff[0]
        for k, v in self.data.iteritems():
            if v == last:
                return k
        raise Exception("This should never happen")

    def put(self, frame, **kwargs):
        super(Lru, self).put(frame, **kwargs)
        self.fill_buff(frame)

    def swap(self, frame, **kwargs):
        self.swaps += 1
        return self.last_used()


class Alru(Algo):
    def __init__(self, count):
        super(Alru, self).__init__(count)
        self.buff = {}

    def put(self, frame, **kwargs):
        if not self.exists(frame):
            key = self.find_key(frame, **kwargs)
            self.data[key] = frame
            self.buff[frame] = 0
        else:
            self.buff[frame] = 1

    def swap(self, frame, **kwargs):
        self.swaps += 1
        found = False
        while not found:
            result = self.last_swapped
            self.last_swapped += 1
            self.last_swapped %= len(self.data)
            frm = self.data[result]
            if self.buff[frm] == 0:
                self.buff.pop(frm)
                return result
            else:
                self.buff[frm] = 0



class Rand(Algo):
    def swap(self, frame, **kwargs):
        self.swaps += 1
        return random.choice(self.data.keys())
__author__ = 'Janek Krukowski'

from collections import namedtuple
import random

random.seed()
Frame = namedtuple('Frame', 'number')


def get_calls(*args):
    return [Frame(number=i) for i in args]


def single_call(r, count):
    num = random.randint(0, r)
    for i in xrange(count):
        lower = num - r if num - r > 0 else 0
        result = random.randrange(lower, num + r)
        yield Frame(number=result)
        num = result

def get_random_calls(r, count=1000):
    return [i for i in single_call(r, count)]


class Algo(object):
    """Base class for algorithms"""

    def __init__(self, count):
        self.swaps = 0
        self.last_swapped = 0
        self.count = count
        self.data = [None for i in xrange(count)]

    def find_key(self, frame, **kwargs):
        for index, item in enumerate(self.data):
            if not item:
                self.swaps += 1
                return index
        return self.swap(frame, **kwargs)

    def exists(self, frame):
        return frame in set(self.data)

    def put(self, frame, **kwargs):
        key = None
        if not self.exists(frame):
            key = self.find_key(frame, **kwargs)
            self.data[key] = frame
        return key

    def extend(self, count):
        self.data.extend([None for i in xrange(count)])

    def shrink(self, count):
        if count >= len(self.data):
            raise ValueError("Cannot shrink by {0}, frame length is {1}".format(count, len(self.data)))
        for i in xrange(count):
            self.data.pop()

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
    def get_furthest(self, tail):
        index = []
        for i in self.data:
            try:
                index.append(tail.index(i))
            except ValueError:
                index.append(len(tail) + 1)
        return sorted(zip(self.data, index), key=lambda x: x[1], reverse=True)[0][0]

    def swap(self, frame, **kwargs):
        self.swaps += 1
        return self.data.index(self.get_furthest(kwargs['tail']))


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
        return self.data.index(self.buff[0])

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
        return random.randrange(self.count)
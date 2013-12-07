__author__ = 'Janek Krukowski'

from collections import namedtuple, deque
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


class Buff(object):
    def __init__(self, size):
        self.size = size
        self.buff = deque()
        self.pointer = 0

    def last_used(self):
        if not self.buff:
            raise ValueError("Buffer is empty")
        return self.buff[0]

    def append(self, item):
        if item in self.buff:
            self.buff.remove(item)
            self.buff.append(item)
        else:
            if self.size == len(self.buff):
                self.buff.popleft()
            self.buff.append(item)

    def expand(self, value):
        self.size += value

    def remove(self, item):
        if item is not None:
            self.buff.remove(item)
        self.size -= 1

    def __repr__(self):
        return "<BUFF size:{0} {1}".format(self.size, self.buff)


class Algo(object):
    """Base class for algorithms"""

    def __init__(self, count):
        self.swaps = 0
        self.last_swapped = 0
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

    def set_frame_length(self, length):
        val = length - len(self)
        if val > 0:
            self.data.extend([None for i in xrange(val)])
        else:
            for i in xrange(abs(val)):
                self.data.pop()

    def swap(self, frame, **kwargs):
        raise NotImplementedError()

    def __len__(self):
        return len(self.data)


class Fifo(Algo):
    def swap(self, frame, **kwargs):
        self.swaps += 1
        result = self.last_swapped
        self.last_swapped += 1
        self.last_swapped %= len(self)
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
        self.buff = Buff(count)

    def last_used(self):
        return self.data.index(self.buff.last_used())

    def put(self, frame, **kwargs):
        super(Lru, self).put(frame, **kwargs)
        self.buff.append(frame)

    def swap(self, frame, **kwargs):
        self.swaps += 1
        return self.last_used()

    def set_frame_length(self, length):
        val = length - len(self)
        if val > 0:
            self.data.extend([None for i in xrange(val)])
            self.buff.expand(val)
        else:
            for i in xrange(abs(val)):
                to_remove = self.data.pop()
                self.buff.remove(to_remove)


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
            self.last_swapped %= len(self)
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
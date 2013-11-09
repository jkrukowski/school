import random

random.seed()


def batch(n, start, stop, delta):
    data = generate_data(n, start, stop)
    result = {}

    fcfs = Fcfs(data)
    while not fcfs.done:
        fcfs.process()
    result['fcfs'] = sum(fcfs.data) / float(len(fcfs.data))

    sjf = Sjf(data)
    while not sjf.done:
        sjf.process()
    result['sjf'] = sum(sjf.data) / float(len(sjf.data))

    rr = Rr(data, delta)
    while not rr.done:
        rr.process()
    result['rr'] = sum(rr.data) / float(len(rr.data))
    return result


def generate_data(n, start=1, stop=30):
    return [random.randint(start, stop) for i in xrange(n)]


class Algo(object):
    def __init__(self):
        self.current = None
        self.data = [0]

    def get(self):
        self.current = self.container.pop()

    def process(self):
        if not self.current:
            self.get()
        else:
            self.current.tick()
        if self.current.finished:
            self.data.append(self.current.wait_time + self.data[-1])
            self.current = None

    @property
    def done(self):
        return not self.container


class Fcfs(Algo):
    def __init__(self, data):
        super(Fcfs, self).__init__()
        self.container = [Process(t) for t in data]

    def get(self):
        self.current = self.container.pop()


class Sjf(Algo):
    def __init__(self, data):
        super(Sjf, self).__init__()
        self.container = [Process(t) for t in sorted(data, reverse=True)]


class Rr(Algo):
    def __init__(self, data, delta):
        super(Rr, self).__init__()
        self.container = [Process(t) for t in data]
        self.delta = delta

    def process(self):
        if not self.current:
            self.get()
        else:
            self.current.tick()
        if self.current.finished or self.current.part_finished(self.delta):
            self.data.append(self.current.wait_time + self.data[-1])
            self.current = None


class Process(object):
    number = 0

    def __init__(self, cpu_length):
        self.cpu_length = cpu_length
        self.wait_time = 0
        self.id = Process.number
        Process.number += 1

    def tick(self):
        self.wait_time += 1

    @property
    def finished(self):
        return self.cpu_length == self.wait_time

    def part_finished(self, value):
        return value == self.wait_time

    def __repr__(self):
        return str(self.cpu_length)


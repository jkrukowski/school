from __future__ import division
import random
from itertools import izip

class Proc(object):
    def __init__(self):
        self.tasks = set()
        self.proc_time = 0

    @property
    def usage(self):
        return sum(t.power for t in self.tasks)

    def add_task(self, task):
        self.tasks.add(task)

    def pop_task(self):
        return self.tasks.pop()

    def tick(self):
        self.proc_time += 1
        to_drop = {i for i in self.tasks if self.proc_time % i.life_length == 0}
        self.tasks = self.tasks - to_drop


class Task(object):
    def __init__(self, power, life_length):
        self.power = power
        self.life_length = life_length

    @classmethod
    def from_random(cls, max_power=20, max_life_length=10):
        power = random.randint(1, max_power)
        life_length = random.randint(1, max_life_length)
        return cls(power, life_length)


class ProcManager(object):
    def __init__(self, n_proc, proc_treshold=75, n=1000):
        self.n_proc = n_proc
        self.proc_treshold = proc_treshold
        self.n = n
        self.procs = [Proc() for i in xrange(n_proc)]
        self.stats = []

    def tick(self):
        for p in self.procs:
            p.tick()

    def run(self):
        for i in xrange(self.n):
            self.process()
            self.add_stats()

    def add_stats(self):
        self.stats.extend([i.usage for i in self.procs])

    def avg(self):
        return sum(self.stats) / len(self.stats)

    def process(self):
        raise NotImplementedError()


class ProcManagerFirst(ProcManager):
    def process(self):
        while True:
            self.tick()
            random.shuffle(self.procs)
            proc = self.procs[0]
            task = Task.from_random()
            for p in self.procs[1:]:
                if p.usage <= self.proc_treshold:
                    p.add_task(task)
                    return
            if proc.usage <= self.proc_treshold:
                proc.add_task(task)
                return


class ProcManagerSecond(ProcManager):
    def process(self):
        while True:
            self.tick()
            random.shuffle(self.procs)
            proc = self.procs[0]
            task = Task.from_random()
            if proc.usage <= self.proc_treshold:
                proc.add_task(task)
                return
            for p in self.procs[1:]:
                if p.usage <= self.proc_treshold:
                    p.add_task(task)
                    return


class ProcManagerThird(ProcManagerSecond):
    def balance(self):
        lower = (i for i in self.procs if i.usage <= self.proc_treshold)
        upper = (i for i in self.procs if i.usage > self.proc_treshold)
        for l, u in izip(lower, upper):
            l.add_task(u.pop_task())

    def process(self):
        self.balance()
        super(ProcManagerThird, self).process()
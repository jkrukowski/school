__author__ = 'Janek Krukowski'

from algo import *
import random
import math
from numpy import histogram
import copy
from itertools import izip, tee, cycle


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def group_edges(data, n):
    k = int(math.sqrt(n))
    _, edges = histogram(data, k)
    return edges


def group(data, edges):
    groups = []
    for lower, upper in pairwise(edges):
        groups.append([p for p in data if lower <= p.size <= upper])
    return groups


def get_process_calls(processes=10, frames=4, min_process_calls=500, max_process_calls=5000):
    return [get_random_calls(frames, random.randint(min_process_calls, max_process_calls)) for i in xrange(processes)]


class Process(Lru):
    def __init__(self, frames_count, calls, allo_type):
        super(Process, self).__init__(frames_count)
        self.calls = calls
        self._initial_size = len(calls)
        self.allo_type = allo_type
        self.pointer = 0

    @property
    def is_done(self):
        return self.pointer == len(self.calls) - 1

    @property
    def size(self):
        return self._initial_size - self.pointer

    @property
    def initial_size(self):
        return self._initial_size

    def reset(self):
        self.pointer = 0

    def put(self):
        if not self.is_done:
            super(Process, self).put(self.calls[self.pointer])
            self.pointer += 1

    def __repr__(self):
        return "<PROCESS: len={0}, init_len={1}, frames={2}>".format(len(self.calls) - self.pointer - 1,
                                                                     len(self.calls),
                                                                     len(self))


class ProcessManager(object):
    def __init__(self, proc_data, process_frames=4, system_frames=40, allo_type="stable"):
        self.proc_data = proc_data
        self.process_count = len(proc_data)
        self.process_frames = process_frames
        self.system_frames = system_frames
        self.allo_type = allo_type
        self.proc_set = self.create_processes()
        if self.allo_type == "prop":
            self.set_process_frames()

    def set_process_frames(self):
        edg = group_edges([proc.size for proc in self.proc_set], self.process_count)
        grp = group(self.proc_set, edg)
        assiged = self.increase_frames(grp, [i + self.process_frames for i in xrange(len(grp))])
        self.decrease_frames(assiged)

    def create_processes(self):
        return {Process(self.process_frames, d, self.allo_type) for d in self.proc_data}

    def increase_frames(self, groups, frames_group):
        assiged = 0
        for gr, fr in izip(groups, frames_group):
            for p in gr:
                p.set_frame_length(fr)
                assiged += fr
        return assiged

    def decrease_frames(self, value):
        proc_list = set(self.proc_set)
        while self.system_frames < value:
            if not proc_list:
                proc_list = set(self.proc_set)
            proc = min(proc_list, key=lambda x: len(x))
            proc.set_frame_length(len(proc) - 1)
            value -= 1
            proc_list.remove(proc)

    def tick(self):
        for proc in self.proc_set:
            proc.put()

    @property
    def swaps(self):
        return sum(p.swaps for p in self.proc_set)

    @property
    def finished(self):
        for p in self.proc_set:
            if not p.is_done:
                return False
        return True

    def __repr__(self):
        "\n".join([str(i) for i in self.proc_set])


if __name__ == "__main__":
    for i in xrange(10000):
        data = get_process_calls()
        proc = {
            "stable": ProcessManager(data, allo_type="stable"),
            "prop": ProcessManager(data, allo_type="prop")
        }
        result = {}
        for n, p in proc.iteritems():
            while not p.finished:
                p.tick()
            result[n] = p.swaps
        print result["stable"] - result["prop"]



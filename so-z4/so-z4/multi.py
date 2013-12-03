__author__ = 'Janek Krukowski'

from algo import *
import random


class Process(object):
    def __init__(self, algo, frames_count, calls):
        self.algo = algo(frames_count)
        self.frames = frames_count
        self.calls = calls
        self._initial_size = len(calls)

    @property
    def is_done(self):
        return not self.calls

    @property
    def size(self):
        return len(self.calls)

    @property
    def initial_size(self):
        return self._initial_size

    @property
    def swaps(self):
        return self.algo.swaps

    def put(self):
        self.algo.put(self.calls.pop())


class ProcessManager(object):
    def __init__(self, process_count=10, process_frames=4, system_frames=60,
                 min_process_calls=500, max_process_calls=5000,
                 swap_algo=Lru, allo_type="stable"):
        self.process_count = process_count
        self.process_frames = process_frames
        self.system_frames = system_frames
        self.min_process_calls = min_process_calls
        self.max_process_calls = max_process_calls
        self.swap_algo = swap_algo
        self.allo_type = allo_type
        self.proc_set = {self.create_process() for i in xrange(self.process_count)}

    def get_process_calls(self):
        return get_random_calls(10, random.randint(self.min_process_calls, self.max_process_calls))

    def get_process_frames(self):
        return self.process_frames

    def create_process(self):
        nframes = self.get_process_frames()
        calls = self.get_process_calls(nframes)
        proc = Process(self.swap_algo, nframes, calls)
        self.proc_set.add(proc)
        return proc

    def tick(self):
        for proc in self.proc_set:
            proc.put()

if __name__ == "__main__":
    pm = ProcessManager()
    pm.tick()

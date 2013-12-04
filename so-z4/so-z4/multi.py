__author__ = 'Janek Krukowski'

from algo import *
import random


class Process(Lru):
    def __init__(self, frames_count, calls):
        super(Process, self).__init__(frames_count)
        self.calls = calls
        self._initial_size = len(calls)
        self.pointer = 0

    @property
    def is_done(self):
        return self.pointer == len(self.calls) - 1

    @property
    def size(self):
        return len(self.calls)

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
                                                                     self.count)


class ProcessManager(object):
    def __init__(self, process_count=2, process_frames=4, system_frames=60,
                 min_process_calls=500, max_process_calls=5000, allo_type="stable"):
        self.process_count = process_count
        self.process_frames = process_frames
        self.system_frames = system_frames
        self.min_process_calls = min_process_calls
        self.max_process_calls = max_process_calls
        self.allo_type = allo_type
        self.proc_set = {self.create_process() for i in xrange(self.process_count)}
        self.set_frames()

    def set_frames(self):
        pass

    def create_process(self):
        calls = get_random_calls(4, random.randint(self.min_process_calls, self.max_process_calls))
        nframes = self.process_frames
        return Process(nframes, calls)

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
    for i in xrange(10):
        pm = ProcessManager()
        while not pm.finished:
            pm.tick()
            print pm
        print pm.swaps


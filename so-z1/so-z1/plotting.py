import sys
import pylab
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import algo
import argparse


class Buff(object):
    def __init__(self, names, nmax=100):
        self.data = defaultdict(deque)
        self.names = set(names)
        self.nmax = nmax

    def add(self, name, value):
        if name not in self.names:
            raise ValueError()
        if len(self.data[name]) > self.nmax:
            self.data[name].popleft()
        self.data[name].append(value)

    def add_batch(self, batch):
        for k, v in batch.iteritems():
            self.add(k, v)

    def __iter__(self):
        for key in self.names:
            yield key, self.data[key]


def main(args):
    buff = Buff(('fcfs', 'sjf', 'rr'))
    pylab.figure()
    plt.ion()
    while True:
        buff.add_batch(algo.batch(n=args.n, start=args.start, stop=args.stop, delta=args.delta))
        plt.pause(0.1)
        plt.clf()
        plt.ylabel('Mean wait time')
        for key, data in buff:
            plt.plot(data, label=key)
        plt.legend()
        plt.draw()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes simlutation')
    parser.add_argument('n', type=int, help='queue length')
    parser.add_argument('start', type=int, help='cpu wait start value')
    parser.add_argument('stop', type=int, help='cpu wait stop value')
    parser.add_argument('delta', type=int, help='rr alg delta value')
    args = parser.parse_args()
    sys.exit(main(args))

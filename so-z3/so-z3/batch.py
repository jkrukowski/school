__author__ = 'Janek Krukowski'
from algo import *


def get_algos(count):
    return {
        "fifo": Fifo(count=count),
        "opt": Opt(count=count),
        "lru": Lru(count=count),
        "alru": Alru(count=count),
        "rand": Rand(count=count)
    }


def put_data(algos, data):
    for index, frame in enumerate(data):
        for key, val in algos.iteritems():
            val.put(frame, tail=data[index + 1:])
    return {key: val.swaps for key, val in algos.iteritems()}


def run(nmax, count, fcount):
    data = get_random_calls(nmax=nmax, count=count)
    algos = get_algos(count=fcount)
    return put_data(algos, data)


if __name__ == "__main__":
    print run(nmax=10, count=1000, fcount=4)
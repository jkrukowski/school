__author__ = 'Janek'
from algo import *

def run():
    data = get_calls(1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5)
    fifo, opt, lru, rand = Fifo(count=4), Opt(count=4), Lru(count=4), Rand(count=4)
    for index, frame in enumerate(data):
        fifo.put(frame)
        opt.put(frame, tail=data[index+1:])
        lru.put(frame)
        rand.put(frame)
    print fifo.swaps, opt.swaps, lru.swaps, rand.swaps



if __name__ == "__main__":
    run()
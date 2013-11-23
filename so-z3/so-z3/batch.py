__author__ = 'Janek'
from algo import *

def run():
    data = get_calls(1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5)
    fifo, opt = Fifo(count=4), Opt(count=4)
    for index, frame in enumerate(data):
        fifo.put(frame)
        opt.put(frame, tail=data[index+1:])
    print fifo.swaps, opt.swaps



if __name__ == "__main__":
    run()
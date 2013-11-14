__author__ = 'Janek Krukowski'
from algo import *


def generate_data():
    return {
        "hd": Hd(200, arg_start=65),
        "data": [Proc(100), Proc(198), Proc(44), Proc(132), Proc(2), Proc(134), Proc(70), Proc(72)],
        "demand": Demand(hd, count=10, arg_data=data)
    }


if __name__ == '__main__':

    algos = [Fcfs, Ssft, Scan, Cscan]
    for a in algos:
        algo = a(hd, demand)
        algo.process()
        print algo.score

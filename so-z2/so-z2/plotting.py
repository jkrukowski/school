__author__ = 'Janek Krukowski'
from algo import *


def generate_data():
    hd = Hd(200, arg_start=65)
    data = [Proc(100), Proc(198), Proc(44), Proc(132), Proc(2), Proc(134), Proc(70), Proc(72)]
    demand = Demand(hd, count=len(data), arg_data=data)
    return hd, data, demand


def generate_data_random(nmax=200):
    hd = Hd(nmax)
    data = [Proc.from_random(nmax) for i in xrange(10)]
    demand = Demand(hd, count=len(data), arg_data=data)
    return hd, data, demand


def process(hd, data, demand):
    algos = [Fcfs, Ssft, Scan, Cscan]
    real_algos = [(Edf, Fcfs), (Fdscan, Fcfs)]
    result = {}
    for a in algos:
        algo = a(hd, demand)
        algo.process()
        result[algo.name] = algo.score
    for i, j in real_algos:
        algo = i(j, hd, demand)
        algo.process()
        result[algo.name] = algo.score
    return result, hd, data, demand


def batch(rnd=False):
    if rnd:
        hd, data, demand = generate_data_random()
    else:
        hd, data, demand = generate_data()
    return process(hd, data, demand)

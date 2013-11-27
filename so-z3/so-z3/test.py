__author__ = 'Janek Krukowski'

from algo import *
from batch import get_algos, put_data
from nose.tools import eq_
import random


def test_call_equlas_frames():
    count = random.randint(0, 1000)
    data = get_calls(*[i for i in xrange(count)])
    score = put_data(get_algos(count), data)
    for key, val in score.iteritems():
        eq_(val, count)


def test_known_data():
    data = get_calls(1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5)
    score = put_data(get_algos(4), data)
    eq_(score["fifo"], 10)
    eq_(score["opt"], 6)
    eq_(score["lru"], 8)
    eq_(score["alru"], 8)


def test_repeated_frames():
    count = 4
    data = get_calls(*[random.randint(0, 1000) for i in xrange(count)] * 1000)
    random.shuffle(data)
    score = put_data(get_algos(count), data)
    for key, val in score.iteritems():
        eq_(val, count)


def test_fifo_small():
    count = 2
    data = get_calls(1, 2, 3, 4)
    fifo = Fifo(count=count)
    for index, item in enumerate(data):
        fifo.put(item)
        eq_(fifo.data[index % count], item)


def test_opt_small():
    count = 2
    data = get_calls(1, 2, 3, 1, 2)
    opt = Opt(count=count)
    for index, item in enumerate(data):
        opt.put(item, tail=data[index + 1:])
        if index == 2:
            eq_(opt.data[0], Frame(number=1))
            eq_(opt.data[1], Frame(number=3))
        elif index == 4:
            eq_(opt.data[0], Frame(number=2))
            eq_(opt.data[1], Frame(number=3))


def test_lru_small():
    count = 4
    data = get_calls(1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5)
    lru = Lru(count=count)
    for index, item in enumerate(data):
        lru.put(item)
        if index == 6:
            eq_(lru.data[2], Frame(number=5))
        elif index == 9:
            eq_(lru.data[3], Frame(number=3))
        elif index == 10:
            eq_(lru.data[2], Frame(number=4))
        elif index == 11:
            eq_(lru.data[0], Frame(number=5))


def test_small_alru():
    count = 2
    data = get_calls(1, 2, 1, 3, 2)
    alru = Alru(count=count)
    for index, item in enumerate(data):
        alru.put(item)
        if index == 3:
            eq_(alru.data[1], Frame(number=3))
        if index == 4:
            eq_(alru.data[0], Frame(number=2))
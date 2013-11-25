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
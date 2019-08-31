from __future__ import absolute_import, unicode_literals

import itertools
import logging
import pickle


###
# Array / List Tools
###

def flatten(lists):
    return list(itertools.chain.from_iterable(lists))


def fill(x, y):
    z = -1 if x - y > 0 else 1
    return list(range(x, y + z, z))


###
# I/O Tools
####

def unpickle(fn):
    try:
        with open(fn, 'rb') as fp:
            return pickle.load(fp, encoding='latin1')
    except TypeError:
        logging.warning('Failed unpickling with encoding, using 2.7 compatible version')
        with open(fn, 'rb') as fp:
            return pickle.load(fp)

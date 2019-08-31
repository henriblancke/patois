from __future__ import absolute_import, unicode_literals

import os
from pandas import read_csv
from .base import PatoisCorpus


class Profanity(PatoisCorpus):
    path = os.path.join(os.path.dirname(__file__), 'datasets/profanity.csv')
    __df = read_csv(path)
    __corpus = __df['profanity'].tolist()

    def __getitem__(self, item):
        if item in self.__corpus:
            return True
        return False

    def __len__(self):
        return self.__df['profanity'].nunique()

    @property
    def corpus(self):
        return self.__corpus

    @property
    def dataframe(self):
        return self.__df

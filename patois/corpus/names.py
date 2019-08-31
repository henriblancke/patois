from __future__ import absolute_import, unicode_literals

import os
from pandas import read_csv
from .base import PatoisCorpus


class Names(PatoisCorpus):
    path = os.path.join(os.path.dirname(__file__), 'datasets/names.csv')
    __df = read_csv(path)[['name', 'common']].set_index('name')
    __corpus = __df.to_dict()['common']

    def __getitem__(self, item):
        try:
            return self.__corpus[item]
        except KeyError:
            # Replace by not-in-lexicon error
            raise KeyError

    def __len__(self):
        # Only words associated with an emotion
        return self.__df.index.nunique()

    @property
    def corpus(self):
        return self.__corpus

    @property
    def dataframe(self):
        return self.__df

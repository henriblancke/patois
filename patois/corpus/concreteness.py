from __future__ import absolute_import, unicode_literals

import os
from pandas import read_csv
from .base import PatoisCorpus


class Concreteness(PatoisCorpus):
    path = os.path.join(os.path.dirname(__file__), 'datasets/ConcretenessLex.csv')
    __df = read_csv(path)[['Word', 'Conc.M']].set_index('Word')
    __corpus = __df.to_dict()['Conc.M']

    def __getitem__(self, item):
        try:
            return self.__corpus[item]
        except KeyError:
            # Replace by not in lexicon error
            raise KeyError

    def __len__(self):
        # Only words associated with an emotion
        return self.__df.index.nunique()

    def concrete(self, item):
        try:
            score = self.__corpus[item]
            if score < 2.5:
                return False
            return True
        except KeyError:
            raise KeyError

    @property
    def corpus(self):
        return self.__corpus

    @property
    def dataframe(self):
        return self.__df

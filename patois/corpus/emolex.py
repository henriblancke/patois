from __future__ import absolute_import, unicode_literals

import os
from pandas import read_csv
from .base import PatoisCorpus


def _construct_dict(frame):
    emo_dict = dict()
    for index, data in frame.groupby('word'):
        associated = list(data['emotion'])
        emo_dict[index] = dict(associated=associated)

    return emo_dict


class EmoLex(PatoisCorpus):
    path = os.path.join(os.path.dirname(__file__), 'datasets/EmoLex.csv')
    __df = read_csv(path)
    __df = __df.set_index(['word', 'emotion'])
    __df = __df[__df['associated'] > 0].reset_index()
    __df = __df[~__df['emotion'].isin(['positive', 'negative'])]
    __emotions = __df['emotion'].unique()
    __corpus = _construct_dict(__df)

    def __getitem__(self, item):
        try:
            return self.__corpus[item]
        except KeyError:
            # Replace by not-in-lexicon error
            raise KeyError

    def __len__(self):
        # Only words associated with an emotion
        return self.__df['word'].nunique()

    @property
    def emotions(self):
        return self.__emotions

    @property
    def corpus(self):
        return self.__corpus

    @property
    def dataframe(self):
        return self.__df

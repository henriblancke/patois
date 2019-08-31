import abc


class PatoisCorpus(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __getitem__(self, item):
        return

    @abc.abstractmethod
    def __len__(self):
        return

    @property
    @abc.abstractmethod
    def corpus(self):
        return

    @property
    def dataframe(self):
        return

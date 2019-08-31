from __future__ import absolute_import, unicode_literals

from spacy.tokens import Doc

from .base import PatoisBase
from .sentence import Sentence
from ..utils.factories import TokenFactory
from ..utils.splitter import split_sentence
from ..utils.helpers import split_into_sentences


class Message(PatoisBase):
    def __init__(self, doc, nlp):
        if not isinstance(doc, Doc):
            raise TypeError("Expected spaCy Doc to initiate this object.")

        for method in dir(doc):
            if method not in ['__class__', 'sents', 'ents', 'noun_chunks', 'has_repvec', 'repvec', 'sentiment']:
                setattr(self, method, getattr(doc, method))

        super(Message, self).__init__()

        self._doc = doc
        self._nlp = nlp

    def __iter__(self):
        for item in range(self.__len__()):
            yield TokenFactory.get(self.__getitem__(item))

    def __str__(self):
        return self.__str__()

    def __len__(self):
        return self.__len__()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Sentence(sentence=self._doc[item.start:item.stop:item.step])
        else:
            return TokenFactory.get(self._doc[item])

    @property
    def sents(self):
        for sentence in split_into_sentences(self._doc.text):
            yield Sentence(sentence=self._nlp(sentence))

    @property
    def noun_chunks(self):
        return self._doc.noun_chunks

    @property
    def ents(self):
        return self._doc.ents

    @property
    def split(self):
        for component in self._get_split_components:
            yield Sentence(**component)

    @property
    def _get_split_components(self):
        components = []
        for sentence in split_into_sentences(self._doc.text):
            components.extend(split_sentence(sentence, self._nlp))
        return components

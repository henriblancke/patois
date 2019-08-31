from __future__ import absolute_import, unicode_literals

from spacy.tokens import Span, Doc

from .base import PatoisBase
from ..utils.factories import TokenFactory
from ..utils.helpers import question_check
from ..utils.verb import verb_check


class Sentence(PatoisBase):
    def __init__(self, **kwargs):

        sentence = kwargs['sentence']

        if not type(sentence) in {Doc, Span}:
            raise TypeError("Expected a spaCy Span or Doc to initiate this object.")

        for method in dir(sentence):
            if method not in ['__class__', 'has_repvec', 'repvec']:
                setattr(self, method, getattr(sentence, method))

        self.relation_next = kwargs.get('relation_next', None)
        self.relation_previous = kwargs.get('relation_previous', None)
        self._sentence = sentence
        super(Sentence, self).__init__()

    def __str__(self):
        return self.__str__()

    def __len__(self):
        return self.__len__()

    def __iter__(self):
        for token in self._sentence:
            yield TokenFactory.get(token)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Sentence(sentence=self._sentence[item.start:item.stop:item.step])
        else:
            return TokenFactory.get(self._sentence[item])

    @property
    def is_question(self):
        return question_check(self._sentence)

    @property
    def has_verb(self):
        return verb_check(self._sentence)

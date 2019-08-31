from __future__ import absolute_import

from ..tokens.verb import Verb
from ..tokens.noun import Noun
from ..tokens.token import Token
from ..tokens.number import Number
from spacy.symbols import NOUN, VERB, NUM


class TokenFactory(object):

    types = {
        NOUN: Noun,
        VERB: Verb,
        NUM: Number
    }

    @classmethod
    def get(cls, token):
        if token.pos in list(cls.types):
            return cls.types[token.pos](token)
        else:
            return Token(token)

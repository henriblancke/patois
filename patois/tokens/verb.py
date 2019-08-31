from __future__ import absolute_import, unicode_literals

from .token import Token
from ..utils.wordnet import WordNet
from ..utils.verb import tense as get_tense
from spacy.tokens import Token as SpacyToken
from ..utils.verb import conjugate as get_conjugation


class Verb(Token, WordNet):
    def __init__(self, token):
        if not isinstance(token, SpacyToken):
            raise TypeError("Expected a Token object, got {}".format(type(token)))

        self.wordnet_pos = u'v'
        super(Verb, self).__init__(token)

    def conjugate(self, tense='inf', negate=False):
        """
            - "inf": infinitive
            - "1sgpres": 1st singular present
            - "2sgpres": 2nd singular present
            - "3sgpres": 3rd singular present
            - "pl": present plural
            - "prog": present participle
            - "1sgpast": 1st singular past
            - "2sgpast": 2nd singular past
            - "3sgpast": 3rd singular past
            - "pastpl": past plural
            - "ppart": past participle
        """
        return get_conjugation(self.text, tense, negate)

    @property
    def tense(self):
        return get_tense(self.text)

    # TODO: Add negate property to know whether a verb is negated or not

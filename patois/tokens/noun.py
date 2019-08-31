from __future__ import absolute_import, unicode_literals

from .token import Token
from ..utils.wordnet import WordNet
from spacy.tokens import Token as SpacyToken
from ..utils.noun import article as get_article


class Noun(Token, WordNet):
    def __init__(self, token):
        if not isinstance(token, SpacyToken):
            raise TypeError("Expected a Token object, got {}".format(type(token)))

        self.wordnet_pos = u'n'
        super(Noun, self).__init__(token)

    @property
    def article(self):
        return get_article(self.text)

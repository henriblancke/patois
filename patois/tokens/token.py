from __future__ import absolute_import, unicode_literals

from ..corpus import Profanity


class Token(object):
    _profanity = Profanity()

    def __init__(self, token):
        self._token = token
        for method in dir(token):
            if method not in ['__class__', 'lefts', 'rights', 'children', 'subtree', 'ancestors', 'conjuncts',
                              'has_repvec', 'repvec']:
                setattr(self, method, getattr(token, method))

    def __repr__(self):
        return self.__str__()

    @property
    def lefts(self):
        return self._token.lefts

    @property
    def rights(self):
        return self._token.rights

    @property
    def children(self):
        return self._token.children

    @property
    def subtree(self):
        return self._token.subtree

    @property
    def ancestors(self):
        return self._token.ancestors

    @property
    def conjuncts(self):
        return self._token.conjuncts

    @property
    def is_profanity(self):
        return self._profanity[self.text]

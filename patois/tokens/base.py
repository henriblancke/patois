from __future__ import absolute_import, unicode_literals

from ..corpus import Names


class PatoisBase(object):
    def pos(self, filter=[]):
        for token in self:
            if not filter:
                yield token
            if filter:
                if token.pos_ in filter:
                    yield token

    def ner(self, filter=[]):
        for token in self:
            if not token.ent_type_:
                continue

            if not filter:
                yield token
            if filter:
                if token.ent_type_ in filter:
                    yield token

    # TODO: Implement ngrams. What would the specific use case for ngrams be for us?
    def ngrams(self, n=1, filter_stops=False, filter_punct=True):
        if n < 1:
            raise ValueError('n must be greater than or equal to 1')

        ngrams_ = (self[i: i + n] for i in range(len(self) - n + 1))
        ngrams_ = (ngram for ngram in ngrams_ if not any(w.is_space for w in ngram))
        if filter_stops is True:
            ngrams_ = (ngram for ngram in ngrams_ if not ngram[0].is_stop and not ngram[-1].is_stop)
        if filter_punct is True:
            ngrams_ = (ngram for ngram in ngrams_ if not any(w.is_punct for w in ngram))

        for ngram in ngrams_:
            yield ngram

    @property
    def remove_punctuations(self):
        for token in self:
            if not token.is_punct:
                yield token

    @property
    def remove_stopwords(self):
        for token in self:
            if not token.is_stop:
                yield token

    @property
    def names(self):
        names = Names()
        for token in self:
            try:
                score = names[token.text.lower()]
                if score >= 0.005:
                    yield token
            except KeyError:
                pass

    # TODO: Implement syntax (constituency) parsing
    def syntax(self):
        raise NotImplemented

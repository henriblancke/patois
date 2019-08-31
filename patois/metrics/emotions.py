from __future__ import absolute_import, unicode_literals

from ..corpus import EmoLex


class Emotions(object):
    _emolex = EmoLex()

    def retrieve(self, doc):
        """
        Returns a dictionary with emotions as keys and percentage emotion in text.
        """
        word_count = 0
        results = dict()
        for token in doc:
            if not token.is_stop or token.is_punct:
                try:
                    associated = self._emolex[token.lemma_]['associated']
                    self._process_emotions(results, associated)
                except KeyError:
                    continue
                word_count += 1

        results = self._calculate_percentage(results, word_count)

        return results

    def _calculate_percentage(self, results, word_count):
        """
        Calculate frequency percentage of emotions.
        """

        for emo in self._emolex.emotions:
            try:
                results[emo] = round((results[emo] / float(word_count)) * 100, 3)
            except KeyError:
                results[emo] = 0.0

        return results

    @staticmethod
    def _process_emotions(results, associated):
        """
        Retrieve emotions for a list of words.
        """
        for emo in associated:
            try:
                results[emo] += 1
            except KeyError:
                results[emo] = 1

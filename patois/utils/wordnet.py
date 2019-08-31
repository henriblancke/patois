from __future__ import unicode_literals

from nltk.corpus import wordnet


class WordNet(object):
    def __init__(self, text, pos):
        # The inheriting class needs to set self.pos
        self.text = text
        self.wordnet_pos = pos

    @property
    def gloss(self, sense=0):
        """
        Returns the dictionary description of the given word.
        """
        s = self._synset(self.text, sense=sense)
        return s.definition()

    @property
    def senses(self):
        """
        Returns all the wordnet senses and their meaning.

        """
        sense_set = wordnet.synsets(self.text)

        result = list()
        for s in sense_set:
            result.append(s.lemma_names())

        return result

    @property
    def lexname(self):
        """
        Retuns a categorization for the given word.
        """
        s = self._synset(self.text)

        if not s:
            return []

        return s.lexname().split('.')[1]

    def hyponym(self, sense=None):
        """
        Returns examples of the given word.
        With sense you can select a certain sense at index x.

        :param word: str
        :param sense: int, default None
        :return: list
        """
        s = self._synset(self.text)

        if not s:
            return []

        hypo = s.hyponyms()

        results = list()
        for h in hypo:
            results.append(h.lemma_names())

        if not sense:
            return results

        # TODO: Exception when not an int
        return results[:sense + 1]

    def hypernym(self, sense=None):
        """
        Returns abstractions of the given word.
        With sense you can select a certain sense at index x.
        """
        s = self._synset(self.text)

        if not s:
            return []

        hyper = s.hypernyms()

        results = list()
        for h in hyper:
            results.append(h.lemma_names())

        if not sense:
            return results

        return results[:sense]

    @property
    def hypernyms(self):
        raise NotImplementedError

    @property
    def holonym(self):
        raise NotImplementedError

    def meronym(self, sense=0):
        """
        Returns the collection in which the word can be found.
        """
        s = self._synset(self.text, sense=sense)

        if not s:
            return []

        return s.member_meronyms()

    def antonym(self, sense=0):
        """
        Returns the semantic opposite of the word
        """
        s = self._synset(self.text, sense=sense)

        if not s:
            return []

        lemmas = s.lemmas()

        result = list()

        for lemma in lemmas:
            if lemma.antonyms():
                result.append(lemma.antonyms()[0].name())

        return result if result else []

    def meet(self, word, sense1=0, sense2=0):
        """
        Returns what the word1 and word2 have in common.
        """
        s1 = self._synset(self.text, sense1)
        s2 = self._synset(word, sense2)

        common = s1.lowest_common_hypernyms(s2)

        result = list()
        for c in common:
            result.append(c.name()[:5])

        return result if result else []

    def _synset(self, word, sense=0):
        return wordnet.synsets(word, pos=self.wordnet_pos)[sense]

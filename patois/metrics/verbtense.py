from __future__ import division, absolute_import, unicode_literals

from ..utils import verb
from collections import Counter


class VerbTense(object):
    tense_lookup = {
        "PAST": "past",
        "PRES": "present",
        "FUTR": "future"
    }

    def retrieve(self, doc):
        """
        Returns a dict with verb tenses (PAST, PRES, FUTR), two metrics, and original message
        """
        tenses = self._get_verb_clause_tenses(doc)

        results = dict(
            message=doc.text,
            **self._get_verb_tense_metric(tenses)
        )

        return results

    def _get_verb_tense_metric(self, tenses):

        metrics = dict()
        counts = dict(Counter(tenses))

        for each in ['PAST', 'PRES', 'FUTR']:
            key = self.tense_lookup[each]

            try:
                metrics[key] = 100 * counts[each] / len(tenses)
            except:
                metrics[key] = 0.

        return metrics

    @staticmethod
    def _get_verb_clause_tenses(doc):
        list_of_verb_phrases = verb.verb_clause_split_tenses(doc)
        results = verb.verb_tense_decider(list_of_verb_phrases)
        return results

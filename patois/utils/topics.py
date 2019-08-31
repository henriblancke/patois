from __future__ import absolute_import, unicode_literals

import os

import numpy as np

from .tools import unpickle
from gensim.models.wrappers.ldamallet import LdaMallet, malletmodel2ldamodel


class Topics(object):
    __dict_path = os.path.join(os.path.dirname(__file__), 'models/mallet-dict.pkl')
    __model_path = os.path.join(os.path.dirname(__file__), 'models/mallet-model.model')
    __mallet_path = os.path.join(os.path.dirname(__file__), 'models/mallet/bin/mallet')
    __topic_file_path = os.path.join(os.path.dirname(__file__), 'models/topic-files/')

    dictionary = unpickle(__dict_path)
    model = LdaMallet.load(__model_path)
    model.mallet_path = __mallet_path
    model.prefix = __topic_file_path

    model_fast = malletmodel2ldamodel(model, 0.1, 1000)

    topic_map = {
        0: 'education',
        1: 'dating',
        2: 'change',
        3: 'communication',
        4: 'broken relationship',  # relationship status
        5: 'finances and accounting',
        6: 'excessive thoughts',
        7: 'politics',
        8: 'financial investments',
        9: 'physical health',
        10: 'work',
        11: 'sleep',
        12: 'emotions',
        13: 'medication regimen',
        14: 'past experiences / decisions',  # or decisions
        15: 'general apathy',
        16: 'NaN', # ignore
        17: 'relocation',
        18: 'social stressors',
        19: 'memories',
        20: 'financial decisions',
        21: 'family',
        22: 'nutrition and weight',
        23: 'relationships',
        24: 'marital issues',
        25: 'religion and belief systems',
        26: 'experiences',
        27: 'financial pressure',
        28: 'romantic relationship',
        29: 'relationship issues',
        30: 'routines',
        31: 'taxes and claims',  # income and benefits
        32: 'symptoms of mental illness',
        33: 'dispute and argument',
        34: 'lack of motivation',
        35: 'reflection and mindfulness',
        36: 'event or festivity',
        37: 'self-harm',  # suicide
        38: 'resources and information',
        39: 'addiction',
        40: 'addiction recovery',
        41: 'leisure'
    }

    def get_topics(self, topics):
        top_topics = topics[:, 1].argsort()[-5:][::-1]

        # TODO: weight down scoring
        scores = 0.
        results = {}
        for idx, entry in enumerate(top_topics):
            topic = int(topics[entry][0])
            score = topics[entry][1]

            if idx == 0 and score <= .1:
                return None

            if scores < .55:
                if self.topic_map[topic] != 'NaN':
                    results[self.topic_map[topic]] = score
                scores += score
            else:
                break

        return results

    # def retrieve(self, doc):
    #    tokens = self.get_tokens(doc)
    #    bow = self.dictionary.doc2bow(tokens)
    #    topics = np.array(self.model[bow])
    #    return self.get_topics(topics)

    def retrieve(self, doc):
        tokens = self.get_tokens(doc)
        bow = self.dictionary.doc2bow(tokens)
        topics = np.array(self.model_fast[bow])
        return self.get_topics(topics)

    @staticmethod
    def get_tokens(doc):
        result = []
        for tok in doc:

            if tok.pos_ in ['IN', 'MD', 'CD']:
                continue

            if tok.is_digit or tok.like_num:
                continue

            if tok.is_punct:
                continue

            elif tok.is_stop:
                continue

            else:
                result.append(tok.text.lower())

        return result

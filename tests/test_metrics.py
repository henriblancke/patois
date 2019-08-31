from __future__ import unicode_literals

from patois import Patois
from patois.metrics import Emotions
from patois.metrics import VerbTense

nlp = Patois()


def test_emotions():
    doc = nlp('This is the first message. It contains some sentences. Each sentence also has tokens.')
    emo = Emotions()
    assert emo.retrieve(doc) == {'anger': 100.0,
                                 'anticipation': 100.0,
                                 'disgust': 100.0,
                                 'fear': 100.0,
                                 'joy': 0.0,
                                 'sadness': 100.0,
                                 'surprise': 0.0,
                                 'trust': 0.0}


def test_verbtense():
    doc = nlp('This is the first message. It contains some sentences. Each sentence also has tokens.')
    verbt = VerbTense()
    assert verbt.retrieve(doc) == {'future': 0.0,
                                   'message': 'This is the first message. It contains some sentences. '
                                              'Each sentence also has tokens.',
                                   'past': 0.0,
                                   'present': 100.0}

    doc = nlp('We will be going to the store. It contains some food.')
    verbt = VerbTense()
    assert verbt.retrieve(doc) == {'future': 50.0,
                                   'message': 'We will be going to the store. It contains some food.',
                                   'past': 0.0,
                                   'present': 50.0}

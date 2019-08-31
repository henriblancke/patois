from __future__ import unicode_literals

from patois import Patois
from patois.corpus import Concreteness
from patois.corpus import EmoLex
from patois.corpus import Names

nlp = Patois()


def test_concreteness():
    concr = Concreteness()

    assert concr['flipper'] == 4.26
    assert len(concr) == 39953
    assert concr.concrete('flipper') == True


def test_emolex():
    emo = EmoLex()

    assert emo['wasting'] == {'associated': ['disgust', 'fear', 'sadness']}
    assert len(emo) == 4463


def test_names():
    names = Names()

    assert names['andrew'] == 0.27
    assert len(names) == 5159

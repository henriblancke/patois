from __future__ import unicode_literals

import pytest
from patois import Patois
from patois.tokens.noun import Noun
from patois.tokens.verb import Verb
from patois.tokens.token import Token
from patois.tokens.number import Number
from patois.tokens.message import Message
from patois.tokens.sentence import Sentence

nlp = Patois()


def test_patois_object():
    messages = [
        "This is the first message. It contains some sentences. Each sentence also has tokens.",
        "This is the first message. It contains some sentences. Each sentence also has tokens."
    ]

    test = nlp(messages)

    with pytest.raises(TypeError):
        nlp(dict(key=messages[1]))

    assert len(test) == 2
    assert isinstance(test[0], Message)
    assert isinstance(next(iter(test)), Message)
    assert isinstance(repr(test), str)


def test_base_object():
    test = nlp("This is America and the city is Seattle")

    with pytest.raises(StopIteration):
        next(iter(test.ner(filter=['PERSON'])))

    assert isinstance(next(iter(test.remove_punctuations)), Token)
    assert next(iter(test.remove_punctuations)).text == u'This'
    assert isinstance(next(iter(test.remove_stopwords)), Token)
    assert next(iter(test.remove_stopwords)).text == u'This'
    # assert isinstance(iter(test.ner()).next(), Token)
    assert isinstance(next(iter(test.pos())), Token)


def test_message_object():
    test = nlp(
        "This is the first message. It contains some sentences. It also must have a name so lets talk about Tom.")

    assert len(test) == 24
    assert isinstance(test.__str__(), str)
    assert next(iter(test)).text == u'This'
    assert next(iter(test.sents)).text == u'This is the first message.'
    assert next(iter(test.noun_chunks)).text == u'the first message'
    # assert iter(test.ents).next().text == u'first'
    assert next(iter(test.names)).text == u'Tom'
    assert next(iter(test.split)).text == u'This is the first message.'
    assert test[1:4].text == u'is the first'
    assert test[1].text == u'is'


def test_sentence_object():
    test = nlp("This is the first message. It contains some sentences. Each sentence also has tokens.")
    sentences = list(test.sents)

    with pytest.raises(TypeError):
        Sentence(u'This is a faulty type')

    assert len(sentences) == 4
    assert isinstance(sentences[0], Sentence)
    assert isinstance(sentences[0][1], Token)
    assert isinstance(next(iter(sentences[0])), Token)
    assert next(iter(sentences[0])).text == u'This'
    assert sentences[0].is_question is False


def test_token_object():
    test = nlp("This sentecne is missspelled.")
    assert isinstance(test.__str__(), str)


def test_noun_object():
    test = nlp("This is a sentence.")
    noun_token = test[3]

    assert isinstance(noun_token, Noun)
    assert noun_token.article == u'a'
    assert noun_token.wordnet_pos == u'n'
    assert noun_token.gloss == u'a string of words satisfying the grammatical rules of a language'
    assert noun_token.lexname == u'communication'
    assert noun_token.meet('word') == [u'abstr']
    assert noun_token.meronym() == []
    assert noun_token.hypernym() == [[u'string_of_words', u'word_string', u'linguistic_string']]


def test_verb_object():
    test = nlp("I have never seen a verb.")
    verb_token = test[1]

    assert isinstance(verb_token, Verb)
    assert verb_token.tense == u'infinitive'
    assert verb_token.conjugate(tense='ppart') == u'had'
    assert verb_token.conjugate(tense='ppart', negate=True) == u"hadn't"
    assert verb_token.gloss == u'have or possess, either in a concrete or an abstract sense'
    assert verb_token.lexname == u'possession'
    assert verb_token.meronym() == []
    assert verb_token.hypernym() == []


def test_number_object():
    test = nlp("This sentence contains the number 3.")
    number_token = test[5]

    assert isinstance(number_token, Number)
    assert number_token.spoken == u'three'
    assert number_token.ordinal == u'3rd'
    assert number_token.thousands == u'trillion'

    test = nlp("This sentence contains the number 3.555.")
    number_token = test[5]

    assert number_token.thousands == u'3.555'

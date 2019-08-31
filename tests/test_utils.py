from __future__ import unicode_literals

from patois import Patois
from patois.utils.datasets.slang import slang_dict
from patois.utils.topics import Topics
from patois.utils.keywords import Keywords
from patois.utils import warnings, verb, tools, helpers, splitter

nlp = Patois()


def test_warnings():
    assert str(warnings.PatoisWarning("Test")) == 'Test'


def test_topics():
    doc = nlp("I have been feeling bad because I broke up with my girlfriend yesterday. I feel devastated. "
              "We had an amazing relationship but it had to come to an end.")

    tops = Topics()

    assert list(tops.retrieve(doc).keys()) == ['broken relationship']


def test_keywords():
    doc = nlp("I have been feeling bad because I broke up with my girlfriend yesterday. I feel devastated... "
              "We had an amazing relationship but it had to come to an end!!")

    keywords = Keywords()
    assert keywords.extract(doc) == ['I',
                                     'have',
                                     'been',
                                     '~##feeling##~',
                                     '~##bad##~',
                                     'because',
                                     'I',
                                     '~##broke##~',
                                     '~##up##~',
                                     'with',
                                     '~##my##~',
                                     '~##girlfriend##~',
                                     'yesterday',
                                     '.',
                                     'I',
                                     '~##feel##~',
                                     '~##devastated##~',
                                     '...',
                                     '~##We##~',
                                     '~##had##~',
                                     'an',
                                     '~##amazing##~',
                                     '~##relationship##~',
                                     'but',
                                     '~##it##~',
                                     '~##had##~',
                                     'to',
                                     '~##come##~',
                                     'to',
                                     'an',
                                     '~##end##~',
                                     '!',
                                     '!']

    assert sorted(keywords.extract(doc, keywords_only=True)) == sorted(['my',
                                                                        'relationship',
                                                                        'devastated',
                                                                        'up',
                                                                        'had',
                                                                        'amazing',
                                                                        'it',
                                                                        'girlfriend',
                                                                        'come',
                                                                        'feel',
                                                                        'end',
                                                                        'bad',
                                                                        'broke',
                                                                        'feeling',
                                                                        'we'])

    assert sorted(keywords.extract(doc, keywords_only=True,
                                   filter_tags=['NN', 'NNS', 'NNP',
                                                'NNPS', 'JJ', 'JJR', 'JJS'])) == sorted(['end',
                                                                                         'amazing',
                                                                                         'girlfriend',
                                                                                         'relationship',
                                                                                         'devastated',
                                                                                         'bad'])


def test_verb_clause_split():
    doc = nlp("It is time to go to the store")
    assert verb.verb_clause_split_numbers(doc) == [[1], [3, 4]]

    doc = nlp("We have not been going to the store")
    assert verb.verb_clause_split_numbers(doc) == [[1, 2, 3, 4]]

    doc = nlp("i have been feeling alright and I have not been wild lately")
    assert verb.verb_clause_split_numbers(doc) == [[1, 2, 3], [7, 8, 9]]

    doc = nlp("Welcome I am eating pasta, have been eating pasta, currently eat pasta, and will always eat pasta")
    assert verb.verb_clause_split_numbers(doc) == [[2, 3], [6, 7, 8], [12], [16, 17, 18]]


def test_verb_tense_decider():
    doc = nlp("Welcome I am eating pasta, have been eating pasta, currently eat pasta, and will always eat pasta")
    splits = verb.verb_clause_split_tenses(doc)
    assert verb.verb_tense_decider(splits) == ['PRES', 'PAST', 'PRES', 'FUTR']

    doc = nlp("It will be time for the bus ride. I am already having an excellent time")
    splits = verb.verb_clause_split_tenses(doc)
    assert verb.verb_tense_decider(splits) == ['FUTR', 'PRES']

    doc = nlp("I am having a good day but it has been ok. Where are you? I'll never be there.")
    splits = verb.verb_clause_split_tenses(doc)
    assert verb.verb_tense_decider(splits) == ['PRES', 'PAST', 'PRES', 'FUTR']


def test_question_check():
    doc = nlp("Where are we going today?")
    assert helpers.question_check(doc) is True

    doc = nlp("Are we going today?")
    assert helpers.question_check(doc) is True

    doc = nlp("Are we going today")
    assert helpers.question_check(doc) is False

    doc = nlp("When are we going")
    assert helpers.question_check(doc) is True

    doc = nlp("is it a good day today")
    assert helpers.question_check(doc) is True

    doc = nlp("I am super mega sad where is the store")
    assert helpers.question_check(doc) is True

    doc = nlp("I am sad what the store has become")
    assert helpers.question_check(doc) is False


def test_verb_check():
    doc = nlp("It is time to leave")
    assert verb.verb_check(doc) is True

    doc = nlp("Hello Andrew")
    assert verb.verb_check(doc) is False

    doc = nlp("Time to leave")
    assert verb.verb_check(doc) is True


def test_expand_contractions():
    # With apostrophe
    text = "I haven't been feeling great lately. It's her's."
    assert helpers.expand_contractions(text) == "I have not been feeling great lately. It is her's."

    # Without apostrophe
    text = "I havent felt great lately. Id be better with music"
    assert helpers.expand_contractions(text) == "I have not felt great lately. I would be better with music"


def test_expand_slang():
    # No capitals
    text = "sup"
    assert helpers.expand(text, slang_dict) == "what is up"

    # Capitals
    text = "I Said SUP"
    assert helpers.expand(text, slang_dict) == "I Said what is up"

    # Capitalized
    text = "I said Sup"
    assert helpers.expand(text, slang_dict) == "I said what is up"


def test_flatten():
    x = [[0, 1], [1, 2], [4, 5]]
    assert tools.flatten(x) == [0, 1, 1, 2, 4, 5]


def test_fill():
    x = [2, 4]
    assert tools.fill(x[0], x[-1]) == [2, 3, 4]
    y = [2]
    assert tools.fill(y[0], y[-1]) == [2]


# def test_splits_adjustments():
#    doc = nlp("i have been feeling alright and I have not been wild lately")
#    splits = [[2, 4], [9, 11]]
#    assert splitter._splits_adjustments(splits, doc) == [[0, 4], [6, 11]]


def test_split_sentence():
    doc = nlp("i have been feeling alright and I have not been wild lately")
    result = splitter.split_sentence(doc.text, nlp)
    assert result[0]['sentence'].text == 'i have been feeling alright'
    assert result[0]['relation_next'].text == 'and'
    assert result[0]['relation_previous'] is None
    assert isinstance(result[1], dict)

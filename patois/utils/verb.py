from __future__ import absolute_import, unicode_literals

import os
from .tools import fill

verb_tenses_keys = {
    "infinitive": 0,
    "1st singular present": 1,
    "2nd singular present": 2,
    "3rd singular present": 3,
    "present plural": 4,
    "present participle": 5,
    "1st singular past": 6,
    "2nd singular past": 7,
    "3rd singular past": 8,
    "past plural": 9,
    "past": 10,
    "past participle": 11
}

verb_tenses_aliases = {
    "inf": "infinitive",
    "1sgpres": "1st singular present",
    "2sgpres": "2nd singular present",
    "3sgpres": "3rd singular present",
    "pl": "present plural",
    "prog": "present participle",
    "1sgpast": "1st singular past",
    "2sgpast": "2nd singular past",
    "3sgpast": "3rd singular past",
    "pastpl": "past plural",
    "ppart": "past participle"
}

# Each verb has morphs for infinitve,
# 3rd singular present, present participle,
# past and past participle.
# Verbs like "be" have other morphs as well
# (i.e. I am, you are, she is, they aren't)
# Additionally, the following verbs can be negated:
# be, can, do, will, must, have, may, need, dare, ought.
verb_tenses = {}

path = os.path.join(os.path.dirname(__file__), 'datasets/verb.txt')
with open(path, "r") as f:
    data = f.readlines()

for i in range(len(data)):
    a = data[i].strip().split(",")
    verb_tenses[a[0]] = a

# Each verb can be lemmatised:
# inflected morphs of the verb point
# to its infinitive in this dictionary.
verb_lemmas = {}
for infinitive in verb_tenses:
    for tense in verb_tenses[infinitive]:
        if tense != "":
            verb_lemmas[tense] = infinitive


def infinitive(verb):
    """
    Returns the uninflected form of the verb.

    >>> infinitive('having')
    'have'

    :param verb: str
    :return: str
    """
    try:
        return verb_lemmas[verb]
    except KeyError:
        return ""


def conjugate(verb, tense="inf", negate=False):
    """
    Inflects the verb to the given tense.

    >>> conjugate('be', '1sgpres')
    'am'
    >>> conjugate('be', 'prog')
    'being'
    >>> conjugate('be', '1sgpast')
    'was'
    >>> conjugate('be', 'ppart')
    'been'
    >>> conjugate('be', '1sgpres', True)
    'am not'

    :param verb: str
    :param tense: str

        - "inf": infinitive
        - "1sgpres": 1st singular present
        - "2sgpres": 2nd singular present
        - "3sgpres": 3rd singular present
        - "pl": present plural
        - "prog": present participle
        - "1sgpast": 1st singular past
        - "2sgpast": 2nd singular past
        - "3sgpast": 3rd singular past
        - "pastpl": past plural
        - "ppart": past participle

    :param negate: boolean
    :return: str
    """
    v = infinitive(verb)
    try:
        i = verb_tenses_keys[verb_tenses_aliases[tense]]
    except KeyError:
        i = verb_tenses_keys[tense]

    if negate is True:
        i += len(verb_tenses_keys)
    return verb_tenses[v][i]


def present(verb, person="", negate=False):
    """
    Inflects the verb in the present tense.

    The person can be specified with 1, 2, 3, "1st", "2nd", "3rd", "plural", "*".
    Some verbs like be, have, must, can be negated.

    :param verb: str
    :param person: int or str

        - "1": 1st singular present
        - "2": 2nd singular present
        - "3": 3rd singular present
        - "*": present plural

    :param negate: boolean
    :return: str
    """
    person = str(person).replace("pl", "*").strip("stndrgural")
    hash = {
        "1": "1st singular present",
        "2": "2nd singular present",
        "3": "3rd singular present",
        "*": "present plural",
    }
    if person in hash and conjugate(verb, hash[person], negate) != "":
        return conjugate(verb, hash[person], negate)

    return conjugate(verb, "infinitive", negate)


def present_participle(verb):
    """
    Inflects the verb in the present participle.

    For example: give -> giving, be -> being, swim -> swimming

    :param verb: str
    :return: str
    """
    return conjugate(verb, "present participle")


def past(verb, person="", negate=False):
    """
    Inflects the verb in the past tense.

    The person can be specified with 1, 2, 3, "1st", "2nd", "3rd", "plural", "*".
    Some verbs like be, have, must, can be negated.

    For example: give -> gave, be -> was, swim -> swam

    :param verb: str
    :param person: str

        - "1": 1st singular present
        - "2": 2nd singular present
        - "3": 3rd singular present
        - "*": present plural

    :param negate: boolean
    :return: str
    """
    person = str(person).replace("pl", "*").strip("stndrgural")
    hash = {
        "1": "1st singular past",
        "2": "2nd singular past",
        "3": "3rd singular past",
        "*": "past plural",
    }
    if person in hash and conjugate(verb, hash[person], negate) != "":
        return conjugate(verb, hash[person], negate)

    return conjugate(verb, "past", negate)


def past_participle(verb):
    """
    Inflects the verb in the present participle.

    For example: give -> given, be -> been, swim -> swum

    :param verb: str
    :return: str
    """
    return conjugate(verb, "past participle")


def tenses():
    """
    Returns all possible verb tenses.
    """
    return verb_tenses_keys.keys()


def tense(verb):
    """
    Returns a string from verb_tenses_keys representing the verb's tense.

    >>> tense('given')
    'past participle'

    :param verb: str
    :return: str
    """
    inf = infinitive(verb)
    _ = verb_tenses[inf]
    for tens in verb_tenses_keys:
        if _[verb_tenses_keys[tens]] == verb:
            return tens
        if _[verb_tenses_keys[tens] + len(verb_tenses_keys)] == verb:
            return tens


def is_tense(verb, t):
    """
    Checks whether the verb is in the given tense.

    :param verb: str
    :param t: str - tense
    :return: boolean
    """
    if tense in verb_tenses_aliases:
        t = verb_tenses_aliases[t]
    if tense(verb) == t:
        return True
    else:
        return False


def is_present(verb, person="", negated=False):
    """
    Checks whether the verb is in the present tense.

    :param verb: str
    :param person: str

        - "1": 1st singular present
        - "2": 2nd singular present
        - "3": 3rd singular present
        - "*": present plural

    :param negated: boolean
    :return: boolean
    """
    person = str(person).replace("*", "plural")
    tens = tense(verb)
    if tense is not None:
        if "present" in tens and person in tens:
            if negated is False:
                return True
            elif "n't" in verb or " not" in verb:
                return True

    return False


def is_present_participle(verb):
    """
    Checks whether the verb is in present participle.

    :param verb: str
    :return: boolean
    """
    tens = tense(verb)
    if tens == "present participle":
        return True
    else:
        return False


def is_past(verb, person="", negated=False):
    """
    Checks whether the verb is in the past tense.

    :param verb: str
    :param person: str

        - "1": 1st singular present
        - "2": 2nd singular present
        - "3": 3rd singular present
        - "*": present plural

    :param negated: boolean
    :return: boolean
    """
    person = str(person).replace("*", "plural")
    tens = tense(verb)
    if tens is not None:
        if "past" in tens and person in tens:
            if negated is False:
                return True
            elif "n't" in verb or " not" in verb:
                return True

    return False


def is_past_participle(verb):
    """
    Checks whether the verb is in past participle

    :param verb: str
    :return: boolean
    """
    tens = tense(verb)
    if tens == "past participle":
        return True
    else:
        return False


def _verb_clause_split_helper(doc):
    filtered = list()

    for tok in doc:

        try:
            if tok.pos_ == 'VERB' and str(list(tok.lefts)[-1]) == 'to':
                filtered.append((tok.i - 1, 'to', 'VERB', 'to'))
                filtered.append((tok.i, tok.orth_, tok.pos_, tok.tense))
            elif tok.pos_ == 'VERB':
                filtered.append((tok.i, tok.orth_, tok.pos_, tok.tense))
            elif tok.pos_ not in ['ADV', 'ADJ', 'DET', 'NUM', 'ADP', 'PART']:
                filtered.append((tok.i, tok.orth_, tok.pos_))
            else:
                pass

        except:
            try:

                if tok.pos_ == 'VERB':
                    filtered.append((tok.i, tok.orth_, tok.pos_, tok.tense))
                elif tok.pos_ not in ['ADV', 'ADJ', 'DET', 'NUM', 'ADP', 'PART']:
                    filtered.append((tok.i, tok.orth_, tok.pos_))
                else:
                    pass

            except:
                pass

    return filtered


def verb_clause_split_numbers(doc):
    filtered = _verb_clause_split_helper(doc)

    index = 0
    tmp = list()
    verb_clauses = list()

    while index < len(filtered):
        if filtered[index][2] != 'VERB':
            if tmp:
                verb_clauses.append(tmp)
                tmp = []
        else:
            tmp.append((filtered[index][0]))
        index += 1

    if tmp:
        verb_clauses.append(tmp)

    return [fill(clause[0], clause[-1]) for clause in verb_clauses]


def verb_clause_split_tenses(doc):
    filtered = _verb_clause_split_helper(doc)

    index = 0
    tmp = list()
    verb_clauses = list()

    while index < len(filtered):
        if filtered[index][2] != 'VERB':
            if tmp:
                verb_clauses.append(tmp)
                tmp = []
        else:
            tmp.append((filtered[index][1], filtered[index][3]))
        index += 1

    if tmp:
        verb_clauses.append(tmp)

    return verb_clauses


def verb_tense_decider(list_of_verb_phrases):
    T = list()

    for v in list_of_verb_phrases:

        try:
            first_word = conjugate(v[0][0])
            if first_word == u'be':
                if 'past' in v[0][1].split():
                    T.append('PAST')
                else:
                    if len(v) == 1:
                        T.append('PRES')
                    elif len(v) > 1:
                        if v[1][1] == 'present participle':  # ing gerund
                            if v[1][0] == 'going':
                                T.append('FUTR')
                            else:
                                T.append('PRES')
                        else:
                            T.append('PRES')

            elif first_word == u'have':
                if 'past' in v[0][1].split():
                    T.append('PAST')
                else:
                    if len(v) == 1:
                        T.append('PRES')
                    elif len(v) > 1:
                        if v[1][0] == 'to':
                            T.append('PRES')
                        else:
                            T.append('PAST')
                    else:
                        T.append('ERROR')

            elif first_word == u'will':
                T.append('FUTR')

            elif first_word == u'would':
                if len(v) > 1:
                    if conjugate(v[1][0]) == u'be':
                        T.append('PRES')
                    elif conjugate(v[1][0]) == u'have':
                        T.append('PAST')
                    else:
                        T.append('PRES')
                else:
                    T.append("ERROR")

            elif v[0][1] == 'present participle':
                pass

            else:
                if 'past' in v[0][1].split():
                    T.append('PAST')
                else:
                    T.append('PRES')

        except:
            if T:
                T.append(T[-1])
            else:
                pass

    return T


def verb_check(doc):
    """
    Simple function to check if a text string contains a verb
    """
    verbs = list(doc.pos(filter=['VERB']))
    if verbs:
        return True
    return False

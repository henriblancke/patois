from __future__ import absolute_import, unicode_literals

import re

from .constants import (LINEBREAK_REGEX,
                        URL_REGEX,
                        SHORT_URL_REGEX,
                        EMAIL_REGEX,
                        PHONE_REGEX,
                        NUMBERS_REGEX,
                        CURRENCIES,
                        CURRENCY_REGEX,
                        NONBREAKING_SPACE_REGEX,
                        SPLIT_CAPS,
                        SPLIT_PREFIXES,
                        SPLIT_SUFFIXES,
                        SPLIT_STARTERS,
                        SPLIT_ACRONYMS,
                        SPLIT_WEBSITES)
from .datasets.connectives import commonsense_connectives


###
# Text Preprocessing
###
def expand_contractions(text):
    ###
    # Apostrophe
    ###
    # Split to make readable
    text = re.sub(r"(\b)([Aa]re|[Cc]ould|[Dd]id|[Dd]oes|[Dd]o|[Hh]ad|[Hh]as|[Hh]ave)n't", r"\1\2 not", text)
    text = re.sub(r"(\b)([Ii]s|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]as|[Ww]ere|[Ww]ould|[Oo]ught)n't", r"\1\2 not", text)

    text = re.sub(r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou|[Hh]ow|[Ii]t)'ll", r"\1\2 will", text)
    text = re.sub(r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Yy]ou|[Ww]ho|[Tt]hat)'d", r"\1\2 would", text)
    text = re.sub(r"(\b)([Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'re", r"\1\2 are", text)

    # Split to make readable
    text = re.sub(r"(\b)([Ii]|[Ss]hould|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Ww]ould|[Yy]ou|[Ww]hy|[Ww]ill)'ve", r"\1\2 have",
                  text)
    text = re.sub(r"(\b)([Aa]re|[Cc]ould|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]ould|[Ww]hen|[Ww]here)'ve", r"\1\2 have", text)

    text = re.sub(r"(\b)([Ii]t|[Hh]ow|[Tt]here|[Ww]hat|[Ss]o|[Tt]hat|[Ww]hen|[Ww]here|[Ww]ho|[Ww]hy)'s", r"\1\2 is",
                  text)
    text = re.sub(r"(\b)([Hh]e|[Ss]he|[Ii]t|)'s([\b\s])", r"\1\2 is", text)
    text = re.sub(r"(\b)([Cc]a)n't", r"\1\2n not", text)
    text = re.sub(r"(\b)([Ii])'m", r"\1\2 am", text)
    text = re.sub(r"(\b)([Ll]et)'s", r"\1\2 us", text)
    text = re.sub(r"(\b)([Ww])on't", r"\1\2ill not", text)
    text = re.sub(r"(\b)([Ss])han't", r"\1\2hall not", text)
    text = re.sub(r"(\b)([Yy])(?:'all|a'll)", r"\1\2ou all", text)
    text = re.sub(r"(\b)([Hh]ow|[Ww]here)'d", r"\1\2 did", text)
    text = re.sub(r"(\b)([Ii]t|[Tt]here)'d", r"\1\2 had", text)

    ###
    # No apostrophe
    ###
    # Append trailing whitespace to process messages like I cant, I wont, etc.
    text += " "

    # Split to make readable
    text = re.sub(r"(\b)([Aa]re|[Cc]ould|[Dd]id|[Dd]oes|[Dd]o|[Hh]ad|[Hh]as|[Hh]ave)nt ", r"\1\2 not ", text)
    text = re.sub(r"(\b)([Ii]s|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]as|[Ww]ere|[Ww]ould|[Oo]ught)nt", r"\1\2 not ", text)

    # Exclude he because hell is a word
    text = re.sub(r"(\b)([Ss]he|[Tt]hey|[Ww]hat|[Ww]ho|[Yy]ou|[Hh]ow|[Ii]t)ll ", r"\1\2 will ", text)
    text = re.sub(r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Yy]ou|[Ww]ho|[Tt]hat)d ", r"\1\2 would ", text)
    text = re.sub(r"(\b)([Tt]hey|[Ww]hat|[Ww]ho|[Yy]ou)re ", r"\1\2 are ", text)

    # Split to make readable
    text = re.sub(r"(\b)([Ii]|[Ss]hould|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Ww]ould|[Yy]ou|[Ww]hy|[Ww]ill)ve ", r"\1\2 have ",
                  text)
    text = re.sub(r"(\b)([Aa]re|[Cc]ould|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]ould|[Ww]hen|[Ww]here)ve ", r"\1\2 have ", text)

    text = re.sub(r"(\b)([Ii]t|[Hh]ow|[Tt]here|[Ww]hat|[Tt]hat|[Ww]hen|[Ww]here|[Ww]ho|[Ww]hy)s ", r"\1\2 is ",
                  text)
    text = re.sub(r"(\b)([Cc]a)nt ", r"\1\2n not ", text)
    text = re.sub(r"(\b)([Ii])m ", r"\1\2 am ", text)
    text = re.sub(r"(\b)([Ll]et)s ", r"\1\2 us ", text)
    text = re.sub(r"(\b)([Ww])ont ", r"\1\2ill not ", text)
    text = re.sub(r"(\b)([Ss])hant ", r"\1\2hall not ", text)
    text = re.sub(r"(\b)([Yy])(?:all|all) ", r"\1\2ou all ", text)
    text = re.sub(r"(\b)([Hh]ow|[Ww]here)d ", r"\1\2 did ", text)
    text = re.sub(r"(\b)([Ii]t|[Tt]here)d ", r"\1\2 had ", text)
    return text.strip()


def normalize_punctuations(text):
    double_punct = re.compile(r'([.,/#?!$%^&*;:{}=_`~()-])[.,/#?!$%^&*;:{}=_`~()-]+')
    formatting = re.compile(r"(@[A-Za-z0-9]+)|([^A-Za-z0-9 !,?$%&.' \t])|(\w+:\/\/\S+)")
    text = formatting.sub(' ', text)
    text = double_punct.sub(r'\1', text)
    return text


def normalize_whitespace(text):
    return NONBREAKING_SPACE_REGEX.sub(' ', LINEBREAK_REGEX.sub(r'\n', text)).strip()


def replace_urls(text, replace_with='*URL*'):
    return URL_REGEX.sub(replace_with, SHORT_URL_REGEX.sub(replace_with, text))


def replace_emails(text, replace_with='*EMAIL*'):
    return EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with='*PHONE*'):
    return PHONE_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with='*NUMBER*'):
    return NUMBERS_REGEX.sub(replace_with, text)


def replace_currency_symbols(text, replace_with=None):
    if replace_with is None:
        for k, v in CURRENCIES.items():
            text = text.replace(k, v + ' ')
        return text
    else:
        return CURRENCY_REGEX.sub(replace_with, text + ' ')


def expand(message, specific_dict):
    """
    Based on the dictionary passed through to the function,
    this method replaces any key found with the associated dictionary value

    The addition of a space at the beginning and end of the input message
    ensures that the first and last words are handled the same as if
    they were found in the middle of the message
    """

    words = list(specific_dict)
    word_upper = [word.upper() for word in words]
    word_capital = [" " + word.strip().capitalize() + " " for word in words]
    words.extend(word_upper)
    words.extend(word_capital)

    regex = re.compile('(%s)' % '|'.join(words))

    def replace(match):
        return specific_dict[match.group(0).lower()]

    result = regex.sub(replace, " " + message + " ").strip()

    return result


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(SPLIT_PREFIXES, "\\1<prd>", text)
    text = re.sub(SPLIT_WEBSITES, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + SPLIT_CAPS + "[.] ", " \\1<prd> ", text)
    text = re.sub(SPLIT_ACRONYMS + " " + SPLIT_STARTERS, "\\1<stop> \\2", text)
    text = re.sub(SPLIT_CAPS + "[.]" + SPLIT_CAPS + "[.]" + SPLIT_CAPS + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(SPLIT_CAPS + "[.]" + SPLIT_CAPS + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + SPLIT_SUFFIXES + "[.] " + SPLIT_STARTERS, " \\1<stop> \\2", text)
    text = re.sub(" " + SPLIT_SUFFIXES + "[.]", " \\1<prd>", text)
    text = re.sub(" " + SPLIT_CAPS + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace("..", ".")
    text = text.replace("...", ".")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text += "<stop>"
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


###
# Information Extraction
###

def is_connective(word):
    """
    Guesses whether the word is a connective.

    Connectives are conjunctions such as "and", "or", "but",
    transition signals such as "moreover", "finally",
    and words like "I", "she".

    It's useful to filter out connectives
    when guessing the concept of a piece of text.
    ... you don't want "whatever" to be the most important word
    parsed from a text.
    """
    if word.lower() in commonsense_connectives:
        return True
    else:
        return False


def question_check(doc):
    """
    Simple function to determine whether a text string (clause, sentence, or message) contains a question
    """
    flag = False
    question_words = ['who', 'what', 'which', 'when', 'where', 'why', 'how', 'can',
                      'could', 'whose', 'is', 'should', 'would', 'does', 'do']

    for token in doc:
        if token.is_punct and token.text == '?':
            flag = True

    if doc[0].text.lower() in question_words:
        flag = True

    try:
        # TODO: ensure that the if statement below (doc.sents) doesn't break under specific circumstances
        # TODO: adjust split_message function to better pick up question words in middle of sentences
        for split in doc.split:
            if split.relation_next.text in question_words \
                    or split.relation_previous.text in question_words:
                flag = True
                break
    except:
        pass

    return flag

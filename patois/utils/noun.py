from __future__ import unicode_literals

import re

article_rules = [

    ["euler|hour(?!i)|heir|honest|hono", "an"],  # exceptions: an hour, an honor

    # Abbreviations
    # Strings of capitals starting with a vowel-sound consonant
    # followed by another consonant,
    # and which are not likely to be real words.
    ["(?!FJO|[HLMNS]Y.|RY[EO]|SQU|(F[LR]?|[HL]|MN?|N|RH?|S[CHKLMNPTVW]?|X(YL)?)[AEIOU])[FHLMNRSX][A-Z]", "an"],
    ["^[aefhilmnorsx][.-]", "an"],
    ["^[a-z][.-]", "a"],

    ["^[^aeiouy]", "a"],  # consonants: a bear
    ["^e[uw]", "a"],  # eu like "you": a european
    ["^onc?e", "a"],  # o like "wa": a one-liner
    ["uni([^nmd]|mo)", "a"],  # u like "you": a university
    ["^u[bcfhjkqrst][aeiou]", "a"],  # u like "you": a uterus
    ["^[aeiou]", "an"],  # vowels: an owl
    ["y(b[lor]|cl[ea]|fere|gg|p[ios]|rou|tt)", "an"],  # y like "i": an yclept, a year
    ["", "a"]  # guess "a"

]


def article(word):
    """
    Returns the indefinite article for a given word.

    :param word: str
    :return: str

        - word with article
    """
    for rule in article_rules:
        pattern, art = rule
        if re.search(pattern, word) is not None:
            return art

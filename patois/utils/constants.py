from __future__ import unicode_literals

import re

###
# Text Processing
###

PRONOUN_TAGS = ['PRP', 'PRP$']
NOUN_TAGS = ['NN', 'NNS', 'NNP']
ENITITY_TAGS = ['PERSON', 'NORP', 'FACILITY', 'GPE', 'PRODUCT', 'EVENT', 'WORK_OF_ART']


###
# Text Cleaning
###
CURRENCIES = {u'$': 'USD', u'zł': 'PLN', u'£': 'GBP', u'¥': 'JPY', u'฿': 'THB',
              u'₡': 'CRC', u'₦': 'NGN', u'₩': 'KRW', u'₪': 'ILS', u'₫': 'VND',
              u'€': 'EUR', u'₱': 'PHP', u'₲': 'PYG', u'₴': 'UAH', u'₹': 'INR'}

ACRONYM_REGEX = re.compile(
    r"(?:^|(?<=\W))(?:(?:(?:(?:[A-Z]\.?)+[a-z0-9&/-]?)+(?:[A-Z][s.]?|[0-9]s?))|(?:[0-9](?:\-?[A-Z])+))(?:$|(?=\W))",
    flags=re.UNICODE)
EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}(?:$|(?=\b))",
    flags=re.IGNORECASE | re.UNICODE)
PHONE_REGEX = re.compile(
    r'(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?\d{3}[ .-]?\d{4}(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))')
NUMBERS_REGEX = re.compile(
    r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))')
CURRENCY_REGEX = re.compile('[{0}]+'.format(''.join(CURRENCIES.keys())))

LINEBREAK_REGEX = re.compile(r'((\r\n)|[\n\v])+')
NONBREAKING_SPACE_REGEX = re.compile(r'(?!\n)\s+')

URL_REGEX = re.compile(
    r"(?:^|(?<![\w/.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.UNICODE | re.IGNORECASE)  # source: https://gist.github.com/dperini/729294

SHORT_URL_REGEX = re.compile(
    r"(?:^|(?<![\w/.]))"
    # optional scheme
    r"(?:(?:https?://)?)"
    # domain
    r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}"
    r"/"
    # hash
    r"[^\s.,?!'\"|+]{2,12}"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.IGNORECASE)

SPLIT_CAPS = "([A-Z])"
SPLIT_PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SPLIT_SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
SPLIT_STARTERS = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
SPLIT_ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
SPLIT_WEBSITES = "[.](com|net|org|io|gov)"

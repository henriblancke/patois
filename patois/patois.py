from __future__ import absolute_import, unicode_literals

from ftfy import fix_text

from .tokens.message import Message
from .utils.datasets.slang import slang_dict
from .utils.helpers import normalize_whitespace, expand_contractions, expand
from .utils.warnings import PatoisWarning


class Patois(object):
    def __init__(self, language='en_core_web_sm', preprocess=True):
        import spacy
        self._length = 1
        self._input_text = None
        self._preprocess = preprocess
        self._nlp = spacy.load(name=language)

    def __unicode__(self):
        if self._input_text:
            return u'<Patois: {n} messages>'.format(n=len(self))
        else:
            # TODO: Custom Exception?
            raise PatoisWarning('Empty Patois object!')

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for message in self._input_text:
            yield self._get_message(message)

    def __len__(self):
        return self._length

    def __getitem__(self, item):
        # TODO: Add proper slicing
        return self._get_message(self._input_text[item])

    def __call__(self, text):
        if isinstance(text, list):
            self._length = len(text)
            self._input_text = [fix_text(msg, normalization='NFC') for msg in text]
            return self
        elif self._string_check(text):
            return self._get_message(fix_text(text, normalization='NFC'))
        else:
            raise TypeError('Expected string, unicode or list as input, got {type} instead.'.format(type=type(text)))

    def _get_message(self, message):

        if self._preprocess:
            message = expand(message, slang_dict)
            message = expand_contractions(message)
            message = normalize_whitespace(message)

        doc = self._nlp(message)

        return Message(doc, nlp=self._nlp)

    @staticmethod
    def _string_check(text):
        try:
            return isinstance(text, basestring)
        except NameError:
            return isinstance(text, str)

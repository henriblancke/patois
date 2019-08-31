from __future__ import absolute_import, unicode_literals

from .token import Token
from spacy.tokens import Token as SpacyToken


class Number(Token):
    def __init__(self, token):
        if not isinstance(token, SpacyToken):
            raise TypeError("Expected a Token object, got {}".format(type(token)))

        super(self.__class__, self).__init__(token)

        self.numerals = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
            16: "sixteen",
            17: "seventeen",
            18: "eighteen",
            19: "nineteen",
            20: "twenty",
            30: "thirty",
            40: "forty",
            50: "fifty",
            60: "sixty",
            70: "seventy",
            80: "eighty",
            90: "ninety"
        }

        self.numeral_thousands = ["thousand"]
        self.numeral_thousands.extend([m + "illion" for m in [
            "m",
            "b",
            "tr",
            "quadr",
            "quint",
            "sext",
            "sept",
            "oct",
            "non",
            "dec",
            "undec",
            "duodec",
            "tredec",
            "quattuordec",
            "quindec",
            "sexdec",
            "septemdec",
            "octodec",
            "novemdec",
            "vigint"
        ]])

        self.ordinal_nth = {
            0: "th",
            1: "st",
            2: "nd",
            3: "rd",
            4: "th",
            5: "th",
            6: "th",
            7: "th",
            8: "th",
            9: "th",
            11: "th",
            12: "th",
            13: "th",
        }

        self.ordinal_suffixes = [

            ["ty$", "tieth"],
            ["one$", "first"],
            ["two$", "second"],
            ["three$", "third"],
            ["five$", "fifth"],
            ["eight$", "eighth"],
            ["nine$", "ninth"],
            ["twelve$", "twelfth"],
            ["$", "th"],

        ]

    @property
    def spoken(self):
        """
        Tranforms integers and longs to spoken word.

        :return: str
        """
        try:
            number = float(self.text)
        except ValueError:
            return self.text

        if number < 0:
            if number in self.numerals:
                return self.numerals[number]
            else:
                return "minus " + self._chunk(-number)

        return self._chunk(number)

    @property
    def thousands(self):
        try:
            number = int(self.text)
            return self.numeral_thousands[number]
        except ValueError:
            return self.text

    @property
    def ordinal(self):
        """
        Returns the ordinal word of a given number.
        :return: str
        """
        try:
            number = int(self.text)
        except ValueError:
            return self.text

        if number % 100 in self.ordinal_nth:
            return str(number) + self.ordinal_nth[number % 100]
        else:
            return str(number) + self.ordinal_nth[number % 10]

    def _chunk(self, n):
        """
        Recursively transforms the number to words.

        A number is either in the numerals dictionary,
        smaller than hundred and a combination of numeals separated by a dash
        (for example: twenty-five),
        a multitude of hundred and a remainder,
        a multitude of thousand and a remainder.

        :param n: int
        :return: str
        """
        if n in self.numerals:
            return self.numerals[n]

        ch = str(n)
        remainder = 0

        if n < 100:
            ch = self._chunk((n // 10) * 10) + "-" + self._chunk(n % 10)
            return ch
        elif n < 1000:
            ch = self._chunk(n // 100) + " " + "hundred"
            remainder = n % 100
        else:
            base = 1000
            for i in range(len(self.numeral_thousands)):
                base *= 1000
                if n < base:
                    ch = self._chunk(n // (base / 1000)) + " " + self.numeral_thousands[i]
                    remainder = n % (base / 1000)
                    break

        if remainder:
            if remainder >= 1000:
                separator = ","
            elif remainder <= 100:
                separator = " and"
            else:
                separator = ""
            return ch + separator + " " + self._chunk(remainder)
        else:
            return ch

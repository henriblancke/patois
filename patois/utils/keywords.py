from __future__ import unicode_literals

from .constants import PRONOUN_TAGS, NOUN_TAGS, ENITITY_TAGS


class Keywords(object):
    def extract(self, doc, keywords_only=False, filter_tags=[]):
        words = []
        keywords = []
        for tok in doc:
            if tok.tag_ in PRONOUN_TAGS:
                if tok.dep_ in ['nsubj', 'dobj', 'conj', 'poss', 'pobj'] and not tok.text.lower() == 'i':
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ in NOUN_TAGS:
                if tok.dep_ in ['agent', 'nsubj', 'nsubjpass', 'compound', 'pobj', 'dobj', 'pobj', 'attr']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))

                    has_num, idx = self.check_num(tok)

                    if has_num and idx < len(words):
                        words[idx] = self.highlight(doc[idx])
                        keywords.append((doc[idx].text.lower(), tok.tag_))

                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'JJ':
                if tok.dep_ in ['ROOT', 'attr', 'acomp', 'ccomp', 'conj', 'advmod', 'amod', 'dobj', 'pobj']:

                    if tok.ent_type_ == 'DATE':
                        words.append(tok.text)
                        continue

                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))

                    has_neg, idx = self.check_prev_token_neg(tok)

                    if has_neg:
                        words[idx] = self.highlight(doc[idx])
                        keywords.append((doc[idx].text.lower(), tok.tag_))
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'JJR':
                if tok.dep_ in ['dobj', 'acomp']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'VB':
                if tok.dep_ in ['auxpass', 'ccomp', 'ROOT', 'xcomp', 'advcl', 'conj']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                    self.check_verb_neg(tok, doc, words)
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'VBD':
                if tok.dep_ in ['conj', 'ROOT', 'advcl', 'ccomp']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                    self.check_verb_neg(tok, doc, words)
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'VBG':
                if tok.dep_ in ['pcomp', 'ROOT', 'conj', 'xcomp', 'compound', 'advcl', 'ccomp']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                    self.check_verb_neg(tok, doc, words)
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'VBN':
                if tok.dep_ in ['ccomp', 'ROOT', 'dobj', 'conj']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                    self.check_verb_neg(tok, doc, words)
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'VBP':
                if tok.dep_ in ['ROOT', 'advcl', 'conj']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'VBZ':
                if tok.dep_ in ['ROOT', 'conj']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                    self.check_verb_neg(tok, doc, words)
                    self.check_rp(tok, words)
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'RB':
                if tok.dep_ in ['prep']:
                    words.append(self.highlight(tok))
                    keywords.append((tok.text.lower(), tok.tag_))
                else:
                    words.append(tok.text)

                continue

            elif tok.tag_ == 'RP' and tok.dep_ == 'prt':
                words.append(self.highlight(tok))
                keywords.append((tok.text.lower(), tok.tag_))
                continue

            elif tok.ent_type_ in ENITITY_TAGS:
                words.append(self.highlight(tok))
                keywords.append((tok.text.lower(), tok.tag_))
                continue

            else:
                words.append(tok.text)

        if keywords_only:
            if filter_tags:
                return list(set([key[0] for key in keywords if key[1] in filter_tags]))
            return list(set(key[0] for key in keywords))
        return words

    def check_verb_neg(self, tok, doc, words):
        has_neg, idx = self.check_prev_token_neg(tok)
        if has_neg and idx < len(words):
            words[idx] = self.highlight(doc[idx])

    def check_rp(self, tok, words):
        children = list(tok.children)
        if not children:
            return
        for child in children:
            if child.tag_ == 'RP' and child.dep_ == 'prt':
                if child.i < len(words):
                    words[child.i] = self.highlight(child)
        return

    @staticmethod
    def highlight(tok):
        try:
            tok = tok.text
        except:
            pass

        return '~##' + tok + '##~'

    @staticmethod
    def check_prev_token_neg(tok):
        if tok.nbor(-1).dep_ == 'neg':
            return True, tok.nbor(-1).i
        elif tok.nbor(-2).dep_ == 'neg':
            return True, tok.nbor(-2).i
        return False, None

    @staticmethod
    def check_num(tok):
        children = list(tok.children)
        if not children:
            return False, None
        for child in children:
            if child.dep_ in ['num', 'nummod']:
                return True, child.i

        return False, None

from __future__ import absolute_import, unicode_literals


def split_sentence(sent, nlp):
    sent = nlp(sent)

    # Merge noun chunks into one token
    # Merging noun chunks help to make less parsing mistakes
    for np in list(sent.noun_chunks):
        np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)

    # Important tags
    special_tags = ['DT']
    filter_tags = ['WRB', 'WDT', 'CC', "WP"]
    verb_tags = ['VBD', 'VB', 'VBP', 'VBN', 'VBG', 'VBZ']
    filter_dep_tags = ['punct', 'cc', 'mark', 'advmod', 'nsubjpass']
    tags = ['acl', 'conj', 'advcl', 'npadvmod', 'relcl', 'ccomp', 'parataxis']

    # Get the roots of the sentence
    # Usually there will only be 1 root
    roots = [tok for tok in sent if tok.dep_ == 'ROOT']

    # Get important points in the sentence
    def get_points(root):
        points = []
        for tok in root.subtree:
            if tok.tag_ in verb_tags and tok.dep_ in tags:
                try:
                    check_tags = verb_tags + special_tags
                    if tok.nbor(-1).tag_ in check_tags:
                        if not tok.text.lower() in ['have', 'been']:
                            continue
                    if tok.nbor(1).tag_ in verb_tags:
                        continue
                except IndexError:
                    pass
                points.append(tok)
        return points

    # Split the sentence into phrases
    def split(root):
        points = get_points(root)

        cuts = [root.left_edge.i, root.right_edge.i + 1]
        prev_point = root
        for point in points:
            if point.i > prev_point.i:
                distance = point.i - prev_point.i
            else:
                distance = prev_point.i - point.i

            if distance >= 3:
                if point.left_edge.i == point.right_edge.i:
                    continue
                cuts.extend([point.left_edge.i, point.right_edge.i + 1])

            prev_point = point

        # Sort cuts
        cuts = set(cuts)
        cuts.add(0)
        cuts = sorted(list(cuts))

        # Cuts post processing
        for i, value in enumerate(cuts):
            if not i == len(cuts) - 1:
                if 2 > cuts[i + 1] - value > 0:
                    if sent[i].is_punct or sent[i].is_space:
                        cuts.pop(i)

        # Get slice tuples
        slices = []
        for i, value in enumerate(cuts):
            if not i == len(cuts) - 1:
                slices.append((value, cuts[i + 1]))

        results = []
        for s in slices:
            span = sent[s[0]:s[1]]
            filters = [(tok.i, tok.dep_) for tok in span if tok.dep_ in filter_dep_tags or tok.tag_ in filter_tags]
            results.append((s, filters))

        return results

    def post_process(span, filters):
        if not filters:
            return span, None, None

        relation_next = None
        relation_previous = None
        for index, dep in filters:
            if index == span[0].i:
                if dep == 'cc':
                    relation_previous = span[0]
                    span = span[1:]

                if dep in ['nsubjpass', 'mark']:
                    relation_previous = span[0]

                if span[0].tag_ in filter_tags:
                    relation_previous = span[0]

                if dep == 'punct' and span[0].text in [',', ':']:
                    span = span[1:]
                    # Remove additional whitespace
                    if span[0].is_space:
                        span = span[1:]

            if index == span[-1].i:
                if dep == 'punct' and span[-1].text in [',', ':']:
                    span = span[:-1]

                if dep == 'cc':
                    relation_next = span[-1]
                    span = span[:-1]

                if dep in ['nsubjpass', 'mark']:
                    relation_next = span[-1]

                if span[-1].tag_ in filter_tags:
                    relation_next = span[-1]

        return span, relation_next, relation_previous

    comp = []
    for root in roots:
        result = split(root)

        if not result:
            comp.append({'sentence': sent, 'relation_next': None, 'relation_previous': None})
            continue

        for span, filters in result:
            span = sent[span[0]:span[1]]
            span, rel_next, rel_prev = post_process(span, filters)
            comp.append({'sentence': span, 'relation_next': rel_next, 'relation_previous': rel_prev})

    # Set relationships
    for index, entry in enumerate(comp):
        if entry['relation_previous']:
            if index > 0:
                if comp[index - 1]['relation_next'] is None:
                    comp[index - 1]['relation_next'] = entry['relation_previous']

        if entry['relation_next']:
            if index < len(comp) - 1:
                if comp[index + 1]['relation_previous'] is None:
                    comp[index + 1]['relation_previous'] = entry['relation_next']

        if entry['sentence'].text in ['', ' ']:
            comp.pop(index)

    return comp

===============
Language Tricks
===============

Some language capabilities are available at the highest level of the language api.


High level methods
==================

.. autofunction:: patois.language.spell

.. autofunction:: patois.language.tag

Examples
--------

.. code-block:: python

    from patois import language

    # Spelling
    language.spell('wrod')
    language.spell('Miss spelld sentence.')

    # Tagging
    language.tag('Tag me please', 'pos')
    language.tag('I live in France.', 'ner')




Noun
====

Noun related logic.

Module contents
---------------

.. automodule:: patois.language.noun.article
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: patois.language.noun.plural
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: patois.language.noun.singular
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: patois.language.noun.wordnet
    :members:
    :undoc-members:
    :show-inheritance:

Number
======

Number related logic.

Module contents
---------------

.. automodule:: patois.language.number.numeral
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: patois.language.number.ordinal
    :members:
    :undoc-members:
    :show-inheritance:

Verb
====

Verb related logic.

Module contents
---------------

.. automodule:: patois.language.verb.verb
    :members:
    :undoc-members:
    :show-inheritance:
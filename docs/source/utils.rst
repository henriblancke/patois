=======
Helpers
=======

More helpful functions to make our lives easier.

.. note::

    The utils module is not automagically imported with the package, so it has to be imported manually.

ASCII Folding
=============

.. autofunction:: patois.utils.folding

Example
-------

.. code-block:: python

    from partois import utils

    # ASCII folding
    utils.folding('This is my ç')

N-Grams
=======
.. autofunction:: patois.utils.get_ngrams

.. code-block:: python

    # Getting n-grams
    utils.get_ngrams('Return me the n-grams of this sentence')


Keywords
========

.. autofunction:: patois.utils.sentence_keywords

Example
-------

.. code-block:: python

    # Getting n-grams
    utils.get_ngrams('Return me the n-grams of this sentence')


Connective
==========

.. autofunction:: patois.utils.is_connective
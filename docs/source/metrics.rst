==============
Metrics Tricks
==============


Sentiment
=========

Retrieve the sentiment of a message or sentence.

.. autofunction:: patois.metrics.sentiment

Example
-------

.. code-block:: python

    from patois import metrics

    # Sentiment
    ## Get sentiment of entire message
    metrics.sentiment('This is sentence 1. This is sentence 2.')

    ## Get sentiment of each sentence in the message
    metrics.sentiment('This is sentence 1. This is sentence 2.', split=True)


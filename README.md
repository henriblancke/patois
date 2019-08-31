## Patois


> Pronounced: `paˌtwä`

**noun**

>the dialect of the common people of a region, differing in various respects from the standard language of the rest of the country.
"the nurse talked to me in a patois that even Italians would have had difficulty in understanding"
synonyms:	vernacular, (local) dialect, regional language; More
>- the jargon or informal speech used by a particular social group.
"the raunchy patois of inner-city kids"

### What is Patois?

> Patois is a shared library and toolbox for NLP

### Installation

Use the makefile to install/reinstall patois.

* Installing **Patois** for the first time 

When you install patois for the first time you'll have to download the right corpora and language models
```bash
# Install patois
make install
```

* Installing Patois for **development**
```bash
# Install patois
make develop
```

* Testing the Patois **Docker** image
```
make docker-build
```

### Running tests

* Running the tests
```bash
make test
```

* Uploading the coverage file to code-climate
```bash
make submit-coverage
```

### Basic Usage

```python
from patois import Patois

# Init a patois object
# All objects inherit basic spaCy capabilities like pos, dep, ner, etc.
nlp = Patois()

# Give patois a couple of messages
doc = nlp(["Message 1", "Message 2"])
len(doc)
>>> 2

# Iterate through the messages
for message in doc:
    print message # returns a message object

iter(message).next()

# By passing one message you immediately get a Message object
message = nlp("This is a test message, with a number: 3")

# Iterate through sentences
for sentence in message.sentences:
    print sentence # returns a Sentence object
    
# Iterate through tokens
for token in message:
    print token # retuns Noun, Verb, Number or Token object
    
# Iterate through tokens of a sentence
for token in sentence:
    print token # retuns Noun, Verb, Number or Token object

# All objects allow slicing
message[0]
>>> This

# Depending on POS you get a different Token object
verb = message[1]
verb.conjugate('ppart')
>>> u'been'
verb.tense
>>> u'3rd singular present'

noun = message[4]
noun.article
>>> u'a'
noun.lexname
>>> u'communication'
noun.gloss
>>> u'a communication (usually brief) that is written or spoken or signaled'

number = message[10]
number.spoken
>>> u'three'
```

For more examples generate the documentation.

### Documentation

Sphinx is required to generate the documentation. 

```bash
# Install sphinx
pip install sphinx

# Generate the docs
make documentation
```

### Roadmap
- Keep capitals when expand contractions and slang (will improve sentiment)
- Improve topic modelling
    - Better text cleaning
    - Better text replacement (numbers, urls, usernames)
    - Adjust vocabulary size to obtain better results
- Replace gensim word2vec with raw lookup table and vectors
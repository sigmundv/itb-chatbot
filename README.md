# A no-name chatbot
#### For completion of Assignment 1 in the course Natural Language Processing, delivered by Kyle Goslin at ITB Autumn/Winter 2018

## Introduction

This is a simple chatbot with two main features:

1. The ability answer fact-based questions using Wikipedia as an information source
    other data source can be added without too much difficulty
2. The ability answer simple conversational queries such as "how are you today?"

The information retrieval for the fact-based answers is done by searching Wikipedia
using keywords pulled out from the query, then parsing the result using
the Python module BeautifulSoup, and finally calculating the Jaccard similarity for
each of the sentences in the retrieved Wikipedia pages and returning the sentence
most similar to the query.

The conversational part is implemented by using the chatterbot-corpus
to generate a tf-idf model and get the cosine similarities between the sentences
in the corpus and the query sentence, e.g. "how are you today?"

Both parts of the bot contain a feedback step that asks the user they are
satisfied with the answer from the bot. This is done by storing the answer,
and in case they are satisfied with the answer it is used if the same query
is asked again, otherwise the answer is filtered out from the list of possible
answers the bot can generate.

### Technologies used

1. Python 3.6 [https://www.python.org/]
2. BeautifulSoup [https://www.crummy.com/software/BeautifulSoup/bs4/doc/]
2. NLTK [https://www.nltk.org/]
3. scikit-learn [https://scikit-learn.org/stable/index.html]
4. chatterbot-corpus [https://github.com/gunthercox/chatterbot-corpus]

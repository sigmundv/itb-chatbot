import string
import requests
import re
import nltk
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# a machine learning base tokenizer included in nltk
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

# a regex expression to clean metadata from Wikipedia articles
sub = re.compile(r"\[\w*\s*\d+\]|\[edit\]|\[update\]|\(listen\)|\[citation needed\]|\.\)")


def get_wikipedia_result(query, answers):
    # we get the top Wikipedia result
    top_result = get_top_wikipedia_result(query)

    # then we use BeautifulSoup to return the first paragraph from the top result
    soup = BeautifulSoup(top_result, "lxml")
    highest_rated_sentence = get_highest_rated_sentence(query, soup, answers)

    return highest_rated_sentence


def get_highest_rated_sentence(query, soup, answers):
    # we find the paragraphs from a Wikipedia article
    p_sentences = [sent for sents in [sent_detector.tokenize(sub.sub('', p.text.strip()))
                                      for p in soup('p')] for sent in sents]

    # but because some articles might not be structured in paragraphs, we also search for div-tags
    div_sentences = [sent for sents in [sent_detector.tokenize(sub.sub('', p.text.strip()))
                                        for p in soup("div", class_="mw-parser-output")] for sent in sents]

    # we calculate the Jaccard similarity between the query and each of the sentences retrieved above
    similarities = [(jaccard_similarity(query, sentence), sentence) for sentence in p_sentences + div_sentences]

    # we sort the similarities while filtering out any previously unsatisfactory answers
    similarities_sorted = sorted([similarity for similarity in similarities
                                  if similarity[0] > 0 and similarity[1] not in answers])

    # we return the sentence with the biggest Jaccard similiarity to the query
    return similarities_sorted[-1][1]


def get_top_wikipedia_result(query):
    # we use the Wikimedia API [https://www.mediawiki.org/w/api.php] to query Wikipedia

    url = "https://en.wikipedia.org/w/api.php"
    params = {"action": "query", "list": "search", "srwhat": "text", "srsearch": query, "format": "json"}

    response = requests.get(url=url, params=params)

    # We get he pageid of the first result from the search result passed in above

    top_pageid = response.json()["query"]["search"][0]["pageid"]

    # and finally we use the Wikimedia API again to get
    # and return the content of the page with the pageid we fetched above

    params = {"action": "parse", "pageid": top_pageid, "format": "json"}
    top_article = requests.get(url=url, params=params).json()

    return top_article["parse"]["title"], top_article["parse"]["text"]['*']


def jaccard_similarity(str1, str2):
    # calculate the Jaccard similarity between two strings

    a = set(str1.lower().split())  # make a set containing the words from str1
    b = set(str2.lower().split())  # a set containing the words from str2

    return len(a & b) / len(a | b)  # the size of the intersection divided by the size of the union


def scan_corpus(query, corpus, answers):
    # initialize a dictionary of questions from the chatterbox corpus

    question_dict = {}

    # populate this dictionary, grouping together answers that belong to the same question in the corpus
    [question_dict.setdefault(item[0], []).append(item[1:]) for items in corpus for item in items]

    # the grouping above leaves the dictionary values as lists of lists, where each of the inner list contains
    # an answer to a given question
    # therefore we rebuild the dictionary with the dictionary value lists flattened
    question_dict = {key: [item for items in value for item in items] for key, value in question_dict.items()
                     if value not in answers}

    # extract the questions from the corpus as dictionary keys
    # and append the query to the end
    questions = [k.lower() for k in question_dict.keys()]
    questions.append(' '.join(query))

    # initialize tf-idf vectorizer from scikit learn
    vectorizer = TfidfVectorizer(tokenizer=tokenize)

    # fit the vectorizer to the corpus of questions extracted above
    tfidf = vectorizer.fit_transform(questions)

    # calculate the cosine similarity between the query and the rest of the corpus using a function from scikit learn
    similarities = cosine_similarity(tfidf[-1], tfidf)

    # the similarity matrix is returned in a numpy array,
    # and we use the argsort() method to return a list of indices that would sort the similarity array
    # and pick out the index that would yield the second highest similarity
    # (because our own query is included in the similarity matrix, it will be the highest one, so we take the second
    # highest)
    idx = similarities.argsort()[0][-2]

    # we flatten the similarity matrix and sort it
    # this will be used to find out if any similarity greater than 0
    # was returned
    flat_similarities = similarities.flatten()
    flat_similarities.sort()

    # pick out the answer from the question dictionary above
    # for simplicity's sake we pick out the first answer, but this could be improved
    answer = [v[0] for k, v in question_dict.items() if questions[idx] in k.lower()]

    # if the highest similarity is 0, tell the user that we don't understand them
    # otherwise return the answer
    if flat_similarities[-2] == 0:
        return "I am sorry, I don't understand you!"
    else:
        return answer[0]


def tokenize(sentence):
    # a tokenizer for use in scikit learn's TfidfVectorizer function
    # it transforms the sentence to lowercase and removes punctuation before tokenizing it

    return nltk.word_tokenize(sentence.lower().translate(str.maketrans('', '', string.punctuation)))

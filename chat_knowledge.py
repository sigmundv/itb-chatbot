import chat_data_manipulation
from chatterbot_corpus import corpus


def get_question_knowledge(query, answers=[]):
    # we get the knowledge for the answer by searching a data source; in this case we have only implemented Wikipedia

    return search(query, answers, "wikipedia")


def get_conversation_knowledge(query, corpus, answers=[]):
    # we search the chatterbox corpus for an answer if the query is a conversational one

    return lookup(query, corpus, answers)


def lookup(query, corpus, answers):
    return process_corpus(query, corpus, answers)


def process_corpus(query, corpus, answers):
    return chat_data_manipulation.scan_corpus(query, corpus, answers)


def search(query, answers, source):
    if "wikipedia" in source.lower():
        # we make a Wikipedia search and return the result
        return wikipedia_search(query, answers)


def wikipedia_search(query, answers):
    # we get the results from Wikipedia

    return chat_data_manipulation.get_wikipedia_result(query, answers)


def load_conversation_corpus():
    # function to load in the English chatterbox corpus
    # the load_corpus function is included in the chatterbox corpus
    # https://github.com/gunthercox/chatterbot-corpus

    return corpus.load_corpus("chatterbot_corpus.data.english")

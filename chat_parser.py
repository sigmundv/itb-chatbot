import nltk
from nltk.corpus import stopwords
import re
import requests
import country_list
import string

# a translation table for removal of punctuation
remove_punctuation = str.maketrans('', '', string.punctuation)

# load in the list English stopwords included in NLTK
english_stopwords = stopwords.words("english")

# generate a list of countries including the countries in the UK
countries = [item[1].lower() for item in country_list.countries_for_language('en')] \
            + ["england", "northern ireland", "scotland", "wales"]

prep_noun_adj = re.compile(r"^[INJ]")  # POS tags that start with either I, N, or J.
country_names = re.compile(r'|'.join(countries))  # a regex matching any country mentioned above


def parse(entry):
    return parse_query(entry)


def get_context():
    # return the name of the country where your current IP address is located
    return requests.get("http://ipapi.co/country_name").text.lower()


def process_question(tokens):
    # filter out stopwords from the query
    return ' '.join([token for token in tokens if token not in english_stopwords])


def process_conversation(tokens):
    # remove punctuation for the query
    return [token.lower().translate(remove_punctuation) for token in tokens]


def parse_query(query):
    tags = _pos_tag(query)
    tokens = _tokenize(query)

    # if the POS tag is one of WDT, WP, WP$, not VBG, we classify the query as a 'question'
    if tags[0][1].startswith(("WP", "WD")) and "VBG" not in dict(tags).values():

        # if the query does not contain the name of a country, add context
        if not country_names.search(query):
            query = f"{query} {get_context()}"
            tokens = _tokenize(query)

        return {"question": process_question(tokens)}

    # if the criteria above are not met we classify the query as a 'conversation'
    return {"conversation": process_conversation(tokens)}


def _pos_tag(sentence):
    return nltk.pos_tag(_tokenize(sentence))


def _tokenize(sentence):
    return nltk.word_tokenize(sentence)

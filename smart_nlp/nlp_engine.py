import nltk
from rake_nltk import Rake


def get_keywords(text):
    r = Rake()  # Uses stopwords for english from NLTK, and all puntuation characters.
    r.extract_keywords_from_text(text)
    r.get_ranked_phrases()
    return r.ranked_phrases


def tag_sentence(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged_comment = nltk.pos_tag(tokens)
    return tagged_comment


def get_match(tagged_words, tag_previous, tag_after):
    for i, tagged_w in enumerate(tagged_words):
        if tagged_w[1] == tag_previous and tagged_words[i + 1][1] == tag_after:
            return [tagged_words[i][0], tagged_words[i + 1][0]]
    return None

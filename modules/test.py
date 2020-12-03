import nltk

from smart_nlp.nlp_engine import tag_sentence, get_keywords

text = """what is the result of three by five?"""


def match2(token_pos, pos1, pos2):
    for subsen in token_pos:
        # avoid index error and catch last three elements
        end = len(subsen) - 1
        for ind, (a, b) in enumerate(subsen, 1):
            if ind == end:
                break
            if b == pos1 and subsen[ind][1] == pos2:
                yield "{} {}".format(a, subsen[ind][0], subsen[ind + 1][0])


def get_match(tagged_words, tag_previous, tag_after):
    for i, tagged_w in enumerate(tagged_words):
        if tagged_w[1] == tag_previous and tagged_words[i + 1][1] == tag_after:
            return [tagged_words[i][0], tagged_words[i + 1][0]]
    return None


tokens = nltk.word_tokenize(text)
tagged_comment = nltk.pos_tag(tokens)
a = [tagged_comment]

print(a)
print(get_match(tagged_comment,'IN','NN'))
print([(word, tag) for word, tag in tagged_comment if (tag == 'NNP')])

print(get_keywords(text))

from RandomWordGenerator import RandomWord

rw = RandomWord(max_word_size=5)

print(rw.generate())
import smart_nlp.nlp_engine
from nltk.corpus import wordnet


def process(keywords):
    trigger_list = ["meaning", "definition"]
    for tw in trigger_list:
        for kw in keywords:
            if tw in kw:
                return True
    return False


def action(input_module):
    tags_input = smart_nlp.nlp_engine.tag_sentence(input_module)
    tag_params = smart_nlp.nlp_engine.get_match(tags_input, "IN", "NN")
    try:
        if tag_params is not None:
            syns = wordnet.synsets(tag_params[1])[0]
            return "The definition of " + tag_params[1] + " is: " + syns.definition()
        else:
            word = input("Sorry, I am becoming old, can you repeat the word ? ")
            if word.lower() is not "no":
                syns = wordnet.synsets(tag_params[1])[0]
                return "The definition of " + word + " is: " + syns.definition()
    except:
        return "Sorry, I don't know. And maybe I am tired of helping you..."

import nltk
from nltk.stem import WordNetLemmatizer
from modules.module_manager import launch_module, is_master_module
from trainer import Trainer

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
from RandomWordGenerator import RandomWord

model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    prob = ints[0]['probability']
    context = ""
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            context = i['context']
            break

    result_tuple = {
        "tag": tag,
        "text": result,
        "prob": prob,
        "context": context
    }
    return result_tuple


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


def is_tag_in_intents(tag_test):
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag_test:
            return True
    return False


# My custom learn method. Can be better but does the job for now
def learn():
    trainer = Trainer()
    input_l = input("Do you want to create a new intent or update or hot update ? (c/u/hu): ")
    if input_l.lower() == "c":
        new_tag = input("What is the name of the new tag ? ")
        if not is_tag_in_intents(new_tag):
            print("What is the new pattern ? ")
            new_pattern = trainer.get_array_sentences()
            print("What is the new response ? ")
            new_response = trainer.get_array_sentences()
            trainer.add_new_intent(new_tag, new_pattern, new_response)
            print("Your new intent has been created. You will have to restart the neural network to upgrade me.")
        else:
            print("Sorry, i already have this tag, please update it instead.")
    elif input_l.lower() == "u":
        new_tag = input("What is the name of the tag you want to update ? ")
        print(intents)
        if is_tag_in_intents(new_tag):
            print("What is the updated pattern ?")
            new_pattern = trainer.get_array_sentences()
            if len(new_pattern) > 0:
                trainer.add_new_patterns(new_tag, new_pattern)
            print("What is the update response ? ")
            new_response = trainer.get_array_sentences()
            if len(new_response) > 0:
                trainer.add_new_response(new_tag, new_response)
            print("Your intent has been updated. You will have to restart the neural network to upgrade me.")
        else:
            print("Sorry, i don't have this tag, please create it instead.")
    elif input_l.lower() == "hu":
        resp_l = 0
        while resp_l == 0:
            new_tag = input("What is closest from what you said ? ")
            new_resp = chatbot_response(new_tag.lower())
            resp_l = trainer.get_alike_tag(new_resp)
    else:
        print("I will learn next time...")

def correct_previous(previous_input):
    trainer = Trainer()
    print("What is the new response for '"+ previous_input +"' ? ")
    new_response = trainer.get_array_sentences()
    rw = RandomWord(max_word_size=5)
    trainer.add_new_intent(rw.generate(), [previous_input], new_response)
    print("Ok, I will know for next time.")

def intense_learn():
    trainer = Trainer()
    while True:
        rw = RandomWord(max_word_size=5)
        print("What is the new pattern ? ")
        new_pattern = trainer.get_array_sentences()
        print("What is the new response ? ")
        new_response = trainer.get_array_sentences()
        trainer.add_new_intent(rw.generate(), new_pattern, new_response)
        continue_learn = "Your new intent has been created. Continue ? (quit to quit)."
        if continue_learn == "quit":
            break


constant_learn = False
trainer = Trainer()
previous_input = ""
while True:
    inp = input(">>> ")

    if inp.lower() == "quit":
        break
    elif inp.lower() == "learn":
        print("Entering Learn mode ...")
        learn_input = input("What mode ? (periodic - 1 / intense - 2 / constant - 3 / default - quit) >>> ")
        if learn_input == "1":
            learn()
        elif learn_input == "2":
            intense_learn()
        elif learn_input == "3":
            constant_learn = not constant_learn
        print("Leaving Learn mode ...")
    elif inp.lower() == "correct":
        correct_previous(previous_input)
    else:
        master_module = is_master_module(inp.lower())
        if master_module is None:
            resp = chatbot_response(inp.lower())
            if float(resp["prob"]) > 0.7:
                if resp["context"] == "none":
                    print("[" + resp["prob"] + "] " + resp["text"])
                else:
                    resp = launch_module(inp.lower(), resp["context"])
                    print(resp)
                    if constant_learn:
                        revision = input("Answer: " + resp + " - OK for the input: " + inp + " >>> (n/Y)")
                        if revision == "n":
                            resp = trainer.get_array_sentences()
                            rw = RandomWord(max_word_size=5)
                            trainer.add_new_intent(rw.generate(), [inp], resp)

            else:
                print("I am very sorry, but i didn't understand.")
                ans = input("Train new intents : (y/N)")
                if ans.lower() == "y":
                    learn()
        else:
            print(master_module)
    previous_input = inp

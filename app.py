from flask import Flask, render_template, request
import nltk
from nltk.stem import WordNetLemmatizer
from modules.module_manager import launch_module, is_master_module
from trainer import Trainer

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model

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


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    inp = request.args.get('msg')

    master_module = is_master_module(inp.lower())
    if master_module is None:
        resp = chatbot_response(inp.lower())
        if float(resp["prob"]) > 0.7:
            if resp["context"] == "none":
                return resp["text"]
            else:
                resp = launch_module(inp.lower(), resp["context"])
                return resp
        else:
            return "I am very sorry, but i didn't understand."
    else:
        return master_module


if __name__ == "__main__":
    app.run()

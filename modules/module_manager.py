import nltk

import modules.give_time
import modules.give_weather
import modules.give_definition
import modules.give_operation
import smart_nlp.nlp_engine


def is_master_module(input_module):
    # We get the NLP keywords from the input
    keywords = smart_nlp.nlp_engine.get_keywords(input_module)

    if modules.give_weather.process(keywords):
        return modules.give_weather.action(input_module)
    elif modules.give_definition.process(keywords):
        return modules.give_definition.action(input_module)
    elif modules.give_operation.process(input_module):
        return modules.give_operation.action(input_module)
    return None


def launch_module(input_module, context):
    if context == "give_time":
        return modules.give_time.action(input_module)

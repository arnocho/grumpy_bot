import nltk
import pyowm
import smart_nlp.nlp_engine


def process(keywords):
    trigger_list = ["temperature", "weather"]
    for tw in trigger_list:
        for kw in keywords:
            if tw in kw:
                return True
    return False


def action(input_module):
    owm = pyowm.OWM('0886876ca34a4d8d0bbb11a928530cfe')

    tags_input = smart_nlp.nlp_engine.tag_sentence(input_module)
    tag_params = smart_nlp.nlp_engine.get_match(tags_input, "IN", "NNP")
    if tag_params is None:
        tag_params = smart_nlp.nlp_engine.get_match(tags_input, "IN", "NN")
    try:
        if tag_params is not None:
            city = tag_params[1]
            if "temperature" in input_module:
                sf = owm.weather_at_place(city)
                weather = sf.get_weather()
                return "The temperature in " + city + " is " + str(
                    weather.get_temperature('celsius')['temp']) + " degrees"
            else:
                paris = owm.three_hours_forecast(city)
                rain_str = "In " + city + ", you will not have rain"
                if paris.will_have_rain():
                    rain_str = "In " + city + ", you will have rain"

                cloud_str = " with a cloudy sky."
                if paris.will_have_sun():
                    cloud_str = " with a nice sunny sky."

                sf = owm.weather_at_place(city)
                weather = sf.get_weather()
                temperature = " Also, the temperature is currently " + str(
                    weather.get_temperature('celsius')['temp']) + " degrees."
                return rain_str + cloud_str + temperature

        else:
            city = input("For which city ? >>> ")
            if "temperature" in input_module:
                sf = owm.weather_at_place(city)
                weather = sf.get_weather()
                return "The temperature in " + city + " is " + str(
                    weather.get_temperature('celsius')['temp']) + " degrees"
            else:
                paris = owm.three_hours_forecast(city)
                rain_str = "In " + city + ", you will not have rain"
                if paris.will_have_rain():
                    rain_str = "In " + city + ", you will have rain"

                cloud_str = " with a cloudy sky."
                if paris.will_have_sun():
                    cloud_str = " with a nice sunny sky."

                sf = owm.weather_at_place(city)
                weather = sf.get_weather()
                temperature = " Also, the temperature is currently " + str(
                    weather.get_temperature('celsius')['temp']) + " degrees."
                return rain_str + cloud_str + temperature
    except:
        return "Sorry, i faced an issue by fetching the weather."

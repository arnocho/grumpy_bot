from _datetime import datetime
import random


def action(input_module):
    now = datetime.now()
    if "please" in input_module:
        return 'The time is ' + now.strftime('%I:%M %p')
    else:
        rand = random.randint(0, 100)
        if rand < 50:
            return 'The time is ' + now.strftime('%I:%M %p') + '. But next time say please.'
        else:
            return 'The time is ' + now.strftime('%I:%M %p')
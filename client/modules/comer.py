# -*- coding: utf-8-*-
import random
import re

WORDS = ["QUIERO","COMER"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by relaying 
        Quiero Comer

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    messages = ["Comes tu almuerzo"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bquiero comer\b', text, re.IGNORECASE))

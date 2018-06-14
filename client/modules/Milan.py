# -*- coding: utf-8-*-
import random
import re

WORDS = ["A", "C", "MILAN"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by relaying 
        AC Milan

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    messages = ["Milan is the greatest club on earth",
                "You vay merda"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmilan\b', text, re.IGNORECASE))

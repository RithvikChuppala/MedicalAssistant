# -*- coding: utf-8-*-
import random
import re

WORDS = ["PERSON", "TALKING", "YOU"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by relaying the definition of Rithvik Chuppala

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    messages = ["You, Rithvik, are the greatest person to have ever lived",
                "You, Rithvik, are a living legend. One of human kind's greatest ever"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bperson talking to you\b', text, re.IGNORECASE))

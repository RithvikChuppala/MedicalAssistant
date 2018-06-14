import re

from twilio.rest import Client

WORDS = ["I","HAVE","FALLEN"]


def isValid(text):
    return bool(re.search(r'\bi have fallen\b', text, re.IGNORECASE))

def handle(text, mic, profile):
    
    account_sid = profile["TWILIO_ACCOUNT_SID"]
    auth_token = profile["TWILIO_AUTH_TOKEN"]

    client = Client(account_sid, auth_token);
    
    contact_number_one = getContactNumberOne(profile)    
    contact_number_two = getContactNumberTwo(profile)
    contact_number_three = getContactNumberThree(profile)
    my_number = getMyNumber(profile)
   
    sendSMS(mic, client, contact_number_one, contact_number_two, my_number)


def getContactNumberOne(profile):
    return profile["TWILIO_CONTACTS"]["ME"]

def getContactNumberTwo(profile):
    return profile["TWILIO_CONTACTS"]["DAD"]

def getContactNumberThree(profile):
    return profile["TWILIO_CONTACTS"]["MOM"]

def getMyNumber(profile):
    return profile["TWILIO_PHONE_NUMBER"]

def sendSMS(mic, client, to_phone_number_one, to_phone_number_two, from_phone_number):
#    client.messages.create(to=to_phone_number_two, from_=from_phone_number, body="Science Fair voice test run")
    mic.say("Call Sent")
    callone = client.calls.create(to=to_phone_number_one, from_=from_phone_number, url="http://demo.twilio.com/docs/voice.xml")
#    print(callone.sid)
#    calltwo = client.calls.create(to=to_phone_number_two, from_=from_phone_number, url="http://demo.twilio.com/docs/voice.xml")
#    print(calltwo.sid)




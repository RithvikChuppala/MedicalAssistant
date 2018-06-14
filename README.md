Voice command medical asssistant using a pi, speakers, a microphone, and Jasper.

The original Jasper project: https://github.com/jasperproject

I added some additional modules that let you state your symptoms and the system will respond
with possible diagnosis and cures. Another module lets you say a trigger phrase, for example 
"I have fallen". It will then voice call a registered number, using Twilio API's. This module
is also available in Spanish (caido.py), thanks to Google's Voice API's.

The relevant modules for the medical assistant:
symptoms.py
fallen.py
caido.py (in Spanish)
PriaidDiagnosisClient.py


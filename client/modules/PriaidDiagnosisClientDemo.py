#! /usr/bin/python3.4
# -*- coding: utf-8-*-

import PriaidDiagnosisClient
import modules.configg
import random
import sys
import json
import re

WORDS = ["SYMPTOMS"]

def isValid(text):
    return bool(re.search(r'\bsymptoms\b', text, re.IGNORECASE))

def handle(text, mic, profile):
    messages = ["Loading Symptoms Diagnosis"]

    message = random.choice(messages)

    mic.say(message)

    diagnosisClientDemo = PriaidDiagnosisClientDemo()
    diagnosisClientDemo.simulate(mic)

class PriaidDiagnosisClientDemo:
    'Demo class to simulate how to use PriaidDiagnosisClient'

    def __init__(self):
        username = modules.configg.username
        password = modules.configg.password
        authUrl = modules.configg.priaid_authservice_url
        healthUrl = modules.configg.priaid_healthservice_url
        language = modules.configg.language
        self._printRawOutput = modules.configg.pritnRawOutput

        self._diagnosisClient = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)


    def simulate(self, mic):
        # Load body locations
        selectedLocationID = self._loadBodyLocations(mic)
        # Load body sublocations
        selectedSublocationID = self._loadBodySublocations(selectedLocationID, mic)

        # Load body sublocations symptoms
        selectedSymptoms = self._loadSublocationSymptoms(selectedSublocationID, mic)

        # Load diagnosis
        diagnosis = self._loadDiagnosis(selectedSymptoms, mic)

        # Load specialisations
        self._loadSpecialisations(selectedSymptoms, mic)

        # Load issue info
        for issueId in diagnosis:
            self._loadIssueInfo(issueId, mic)

        # Load proposed symptoms
        self._loadProposedSymptoms(selectedSymptoms, mic)


    def _writeHeaderMessage(self, message):
        print("---------------------------------------------")
        print(message)
        print("---------------------------------------------")


    def _writeRawOutput(self, methodName, data):
        print("")
        if self._printRawOutput: 
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            print("Response from method {0}: ".format(methodName))
            print(json.dumps(data))
            print("+++++++++++++++++++++++++++++++++++++++++++++")

    
    def _loadBodyLocations(self, mic):
        bodyLocations = self._diagnosisClient.loadBodyLocations()
        self._writeRawOutput("loadBodyLocations", bodyLocations)

        self._writeHeaderMessage("Body locations:")    
        #for bodyLocation in bodyLocations:
            #print("{0} ({1})".format(bodyLocation["Name"], bodyLocation["ID"]))

        randomLocation = random.choice(bodyLocations)
        self._writeHeaderMessage("Sublocations for randomly selected location {0}".format(randomLocation["Name"]))
	#mic.say("selected location is {0}".format(randomLocation["Name"]))
        return randomLocation["ID"]


    def _loadBodySublocations(self, locId, mic):
        bodySublocations = self._diagnosisClient.loadBodySubLocations(locId)
        self._writeRawOutput("loadBodySubLocations", bodySublocations)

        #for bodySublocation in bodySublocations:
            #print("{0} ({1})".format(bodySublocation["Name"], bodySublocation["ID"]))

        randomSublocation = random.choice(bodySublocations)
        self._writeHeaderMessage("Sublocations for randomly selected location {0}".format(randomSublocation["Name"]))
	#mic.say("selected sublocation is {0}".format(randomSublocation["Name"]))
        return randomSublocation["ID"]


    def _loadSublocationSymptoms(self, subLocId, mic):
        symptoms = self._diagnosisClient.loadSublocationSymptoms(subLocId, PriaidDiagnosisClient.SelectorStatus.Man)
        self._writeRawOutput("loadSublocationSymptoms", symptoms)

        self._writeHeaderMessage("Body sublocations symptoms:")

        for symptom in symptoms:
            print(symptom["Name"])

        randomSymptom = random.choice(symptoms)

        self._writeHeaderMessage("Randomly selected symptom: {0}".format(randomSymptom["Name"]))
	
	#mic.say("Selected symptom is: {0}".format(randomSymptom["Name"]))

        self._loadRedFlag(randomSymptom, mic)

        selectedSymptoms = [randomSymptom]
        return selectedSymptoms


    def _loadDiagnosis(self, selectedSymptoms, mic):
        self._writeHeaderMessage("Diagnosis")
        selectedSymptomsIds = []
        for symptom in selectedSymptoms:
            selectedSymptomsIds.append(symptom["ID"])
            
        diagnosis = self._diagnosisClient.loadDiagnosis(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, 1988)
        self._writeRawOutput("loadDiagnosis", diagnosis)

	##mic.say("Diagnoses are")
	##mic.say(json.dumps(diagnosis))
        
        if not diagnosis:
            self._writeHeaderMessage("No diagnosis results for symptom {0}".format(selectedSymptoms[0]["Name"]))

        for d in diagnosis:
            specialisations = []
            for specialisation in d["Specialisation"]:
                specialisations.append(specialisation["Name"])
            print("{0} - {1}% \nICD: {2}{3}\nSpecialisations : {4}\n".format(d["Issue"]["Name"], d["Issue"]["Accuracy"], d["Issue"]["Icd"], d["Issue"]["IcdName"], ",".join(x for x in specialisations)))

        diagnosisIds = []
        for diagnose in diagnosis:
            diagnosisIds.append(diagnose["Issue"]["ID"])

        return diagnosisIds


    def _loadSpecialisations(self, selectedSymptoms, mic):
        self._writeHeaderMessage("Specialisations")
	#mic.say("Specializations are")
        selectedSymptomsIds = []
        for symptom in selectedSymptoms:
            selectedSymptomsIds.append(symptom["ID"])
            
        specialisations = self._diagnosisClient.loadSpecialisations(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, 1988)
        self._writeRawOutput("loadSpecialisations", specialisations)
                                                                                                     
        for specialisation in specialisations:
            print("{0} - {1}%".format(specialisation["Name"], specialisation["Accuracy"]))
	    #mic.say("{0} - {1}%".format(specialisation["Name"], specialisation["Accuracy"]))


    def _loadRedFlag(self, selectedSymptom, mic):
        redFlag = "Symptom {0} has no red flag".format(selectedSymptom["Name"])
            
        if selectedSymptom["HasRedFlag"]:
            redFlag = self._diagnosisClient.loadRedFlag(selectedSymptom["ID"])
            self._writeRawOutput("loadRedFlag", redFlag)

        self._writeHeaderMessage(redFlag);
	#mic.say(redFlag);


    def _loadIssueInfo(self, issueId, mic):
        issueInfo = self._diagnosisClient.loadIssueInfo(issueId)
        self._writeRawOutput("issueInfo", issueInfo)
        
        self._writeHeaderMessage("Issue info")
	mic.say("Issue info")
	print(issueInfo["Name"].encode('utf-8', 'ignore').strip())
	mic.say("Name")
	mic.say(issueInfo["Name"].encode('utf-8', 'ignore').strip())
	print(issueInfo["ProfName"].encode('utf-8', 'ignore').strip())
	mic.say("Professional Name")
	mic.say(issueInfo["ProfName"].encode('utf-8', 'ignore').strip())
	print(issueInfo["DescriptionShort"].encode('utf-8', 'ignore').strip())
	mic.say("Short Description")
	mic.say(issueInfo["DescriptionShort"].encode('utf-8', 'ignore').strip())
	print(issueInfo["Description"].encode('utf-8', 'ignore').strip())
	mic.say("Description")
	mic.say(issueInfo["Description"].encode('utf-8').strip())
	print(issueInfo["MedicalCondition"].encode('utf-8').strip())
	mic.say("Medical Condition")
	mic.say(issueInfo["MedicalCondition"].encode('utf-8', 'ignore').strip())
	print(issueInfo["TreatmentDescription"].encode('utf-8').strip())
	mic.say("Treatment Description")
	mic.say(issueInfo["TreatmentDescription"].encode('utf-8').strip())
	print(issueInfo["PossibleSymptoms"].encode('utf-8', 'ignore').strip())
	mic.say("Possible Symptoms")
	mic.say(issueInfo["PossibleSymptoms"].encode('utf-8', 'ignore').strip())

    def _loadProposedSymptoms(self, selectedSymptoms, mic):
        selectedSymptomsIds = []
        for symptom in selectedSymptoms:
            selectedSymptomsIds.append(symptom["ID"])
        
        proposedSymptoms = self._diagnosisClient.loadProposedSymptoms(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, 1988)
        self._writeRawOutput("proposedSymptoms", proposedSymptoms)
	mic.say("Proposed symptoms")

        if not proposedSymptoms:
            self._writeHeaderMessage("No proposed symptoms for selected symptom {0}".format(selectedSymptoms[0]["Name"]))
	    mic.say("No proposed symptoms")
            return

        proposedSymptomsIds = []
        for proposeSymptom in proposedSymptoms:
            proposedSymptomsIds.append(proposeSymptom["ID"])
            
        self._writeHeaderMessage("Proposed symptoms: {0}".format(",".join(str(x) for x in proposedSymptomsIds)))
	mic.say("Proposed symptoms: {0}".format(",".join(str(x) for x in proposedSymptomsIds)))


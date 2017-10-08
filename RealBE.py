from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import time
import os
import urllib2
import timeit
import json
import requests
import httplib

A_CLASS_NAME = "61A" #TODO: SET FINAL CLASS NAME
B_CLASS_NAME = "61B" #TODO: SET FINAL CLASS NAME
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "CalHacks-8f56181f7e42.json"
GCS_API_KEY = "AIzaSyBy6MNhLhTbs0vKoBqsoYdyQDq6ceCoNag"
audioURIS = ["gs://calhacksproject/audiofiles/test2.wav"]
delimiters = set([" ", ",", ".", "!", "?"])
AZ_API_KEY = "22c658f2b8784b55aed7e2f689008908"

def processAudio(audioURIS, className=None):
    #Initialize empty topics dictionary RETVAL (will have "topic" : [[List of impotant tokens (summary) with "importance"], [video URLs], [related keywords]] )
    passData = []
    #Convert speech to text (text transcription for each audio file)
    print("\nTRANSCRIBING AUDIO\n")
    transcriptions = transcribeAudio(audioURIS)
    print(transcriptions)
    #Analyze text for keywords
    keywords = []
    print("\nFINDING KEYWORDS AND INFO:\n")
    for i in range(len(audioURIS)):
        audioURI = audioURIS[i]
        transcription = transcriptions[i]
        keywords = getKeyWords(transcription)
        relatedResources = getRelatedResources(keywords)
        passData.append({"Audio_URL":audioURI, "Topics":keywords, "Related_Resources":relatedResources})
    data = {"ClassName":className, "Videos":passData}
    print("Sending post request with info to backend web server server")
    r = requests.post("https://safe-spire-89119.herokuapp.com/api/v1/classes/upload", data=json.dumps(data))



def transcribeAudio(audioURIS):
    """Asynchronously transcribes the audio files specified by the audioURIS."""
    operations=[]
    for audioURI in audioURIS:
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri=audioURI)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, #CHANGE THIS
            sample_rate_hertz=16000, #CHANGE THIS
            language_code='en-US')
        operation = client.long_running_recognize(config, audio)
        operations.append(operation)
    assert len(operations) == len(audioURIS), "An operation was not generated for every ausio file"
    responses = []
    for operation in operations:
        response = operation.result(timeout=600)
        responses.append(response)
    assert len(operations) == len(responses), "Responses were not generated for every operation"
    transcriptions = []
    for response in responses:
        text = ""
        for result in response.results:
            text = text + result.alternatives[0].transcript
        transcriptions.append(text)
    assert len(transcriptions) == len(operations), "A transcription was not generated for evey audio file"
    return transcriptions

def getKeyWords(transcription):
    #Accepts a transcription, splits into <5000 character chunks, runs through keyword search
    #Keeps keywords (up to 7) over .75 in confidence rating
    #Sorts keywords by preference and returns them
    uri = 'westcentralus.api.cognitive.microsoft.com'
    path = '/text/analytics/v2.0/keyPhrases'
    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':AZ_API_KEY} #TODO: Change this
    inputJsons = []
    for i in range(len(transcription)//4900): #TODO: Implement intelligent transcription
        text = transcription[max(0,i*4900):min(len(transcription), (i+1)*4900)]
        inputJsons.append({"language": "en", "id":i+1,"text":text})
    inputJson = {"documents" : inputJsons}
    numDocuments = len(inputJsons)
    print(inputJson)
    """
    req = urllib2.Request('https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases', inputJson, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    """
    body = json.dumps(inputJson)
    conn = httplib.HTTPSConnection(uri)
    conn.request("POST", path, body, headers)
    response = conn.getresponse()
    print("\nRESPONSE READ")
    temp = response.read()
    decoder = json.JSONDecoder()
    obj = decoder.decode(temp)
    print("\nOBJ")
    print(obj)
    keywords =[]
    for i in range(numDocuments):
        keywords = keywords + obj['documents'][i]['keyPhrases']
    print(list(set(keywords)))
    return list(set(keywords))[0:6]

"""
uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/keyPhrases'
def GetKeyPhrases (documents):
    "Gets the sentiments for a set of documents and returns the information."

    headers = {'Ocp-Apim-Subscription-Key': AZ_API_KEY}
    conn = httplib.HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read ()
"""

def getRelatedResources(keywords):
    links = []
    for keyword in keywords:
        resource = keyword.replace(" ", "+")
        links.append("http://www.google.com/search?q=" + resource + "&btnI")
    print(links)
    return links

"""
def processAU(audioURIS):
    #Initialize empty topics dictionary (will have "topic" : [[List of impotant tokens (summary) with "importance"], [video URLs], [related keywords]] )
    topics = {}
    #Convert speech to text (text transcription for each audio file)
    operations=[] # Eache element is [client, operation]
    for audioURI in audioURIS:
        client = speech.SpeechClient()
        operation = client.long_running_recognize(audio=speech.types.RecognitionAudio(uri=audioURI),
        config=speech.types.RecognitionConfig(encoding='FLAC', #TODO: CHANGE THIS
        language_code='en-US',
        sample_rate_hertz=44100)) #TODO: CHANGE THIS
        operations.append(operation)
    retryCount = 0
    for operation in operations:
        operation.poll()
    while retryCount <= 100 and not allOpsComplete(operations):
        if retryCount == 100:
            for operation in operations:
                print(operation.complete) # This line will error
        retryCount += 1
        time.sleep(3*i)
        for operation in operations:
            operation.poll()
    transcriptions = []
    for i in range(len(audioURIS)):
        text = ""
        operation = operations[i]
        for result in operation.results:
            for alternative in result.alternatives:
                text = text + alternative.transcript
        transcriptions.append(text)
    return transcriptions
def allOpsComplete(operations):
    for operation in operations:
        if not operation.complete:
            return False
"""
def gen61afiles():
    return None

def gen61bFiles():
    return None

def runInChunks(files, className):
    return None

def mainProcess():
    print("Generating 61A Filenames")
    sixOneAFiles = gen61aFiles()
    print("Generating 61B FIlenames")
    sixOneBFiles = gen61bFiles()
    print("Starting 61a processing")
    processAudio(sixOneAFiles, className=A_CLASS_NAME)
    print("Starting 61b processing")
    processAudio(sixOneBFiles, className=B_CLASS_NAME)



"""
print ("TESTING")
print("Running sample file (10 mins, LINEAR16, 16kHz)")
start_time = timeit.default_timer()
processAudio(audioURIS, className="TESTING")
elapsed = timeit.default_timer() - start_time
print("TIME ELAPSED:")
print(elapsed)
"""

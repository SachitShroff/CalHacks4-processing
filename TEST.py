import time
from google.cloud import speech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "CalHacks-8f56181f7e42.json"

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Print the first alternative of all the consecutive results.
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
"""

client = speech.SpeechClient()
operation = client.long_running_recognize(
    audio=speech.types.RecognitionAudio(
        uri='gs://calhacksproject/audiofiles/61ALecture1Video1.flac',
    ),
    config=speech.types.RecognitionConfig(
        encoding='FLAC',
        language_code='en-US',
        sample_rate_hertz=44100,
    ),
)
retry_count = 100
while retry_count > 0 and not operation.complete:
    retry_count -= 1
    time.sleep(10)
    operation.poll()  # API call

for result in operation.results:
    for alternative in result.alternatives:
        print('=' * 20)
        print(alternative.transcript)
        print(alternative.confidence)
"""

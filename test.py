# imports
import io
import os
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment

# google authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

# wget -nc https://realenglishconversations.com/...

# instantiate a speech client and declare an audio file
client = speech.SpeechClient()
audio = speech.RecognitionAudio(uri="gs://python-yt/reaction.wav")

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=16000,
    language_code="en-US",
    enable_speaker_diarization=True,
    diarization_speaker_count=2,
)
operation = client.long_running_recognize(config=config, audio=audio)
print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

result = response.results[-1]
words_info = result.alternatives[0].words

words_list = []
# Printing out the output:
for word_info in words_info:
    words_list.append(
        {
            'word': word_info.word,
            'speaker_tag': word_info.speaker_tag,
            'start_time': word_info.start_time,
            'end_time': word_info.end_time,
        }
    )
# print(words_list)

# create a script based on the words_list
current_speaker = words_list[0]['speaker_tag']
current_line = []
script = []

for item in words_list:
    if item['speaker_tag'] != current_speaker:
        # speaker changed, end of line
        script.append(
            {
                'speaker': current_speaker,
                'line': current_line
            }
        )
        current_line = []
        current_speaker = item['speaker_tag']
    else:
        # same speaker, add to the current line
        current_line.append(item['word'])

script.append(
    {
        'speaker': current_speaker,
        'line': current_line
    }
)

script = [print(f"Speaker {line['speaker']}: " + " ".join(line['line'])) for line in script]

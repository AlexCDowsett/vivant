import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os


r = sr.Recognizer()

filename = 'test.wav'

with sr.AudioFile(filename) as source:
    audio_text = r.record(source)

    try:
        text_file = open("Output.txt", "w")
        text_file.write("%s" % r.recognize_google(audio_text))
        text_file.close()
        print('Converting audio to text file')
        #remove this after
        text = r.recognize_google(audio_text)
        print(text)

    except:
        print('This failed!')
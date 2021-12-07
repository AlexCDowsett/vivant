import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

class S2T_fromFile:
    def __init__(self, path):
        self.r = sr.Recognizer()
        self.filename = path
        self.audio_text = ""

    def encode(self): 
        with sr.AudioFile(self.filename) as source:
            recorded_audio = self.r.listen(source)
            print("Done encoding")

        try:
            print("Recognizing text")
            self.audio_text = self.r.recognize_google(
                recorded_audio, 
                language="en-US"
            )
            print("Decoded Text : {}".format(self.audio_text))
            with open("Output.txt", "w") as f:
                f.write(self.audio_text)
                f.close()
                
        except:
            print('This failed!')
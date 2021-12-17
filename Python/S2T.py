import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def main():
    s2t = S2T_fromFile("/home/pi/vivant/s2tBites/out.wav")
    s2t.encode()
    #t2s.play()
    #t2s.remove()

class S2T_fromFile:
    def __init__(self, path):
        self.r = sr.Recognizer()
        self.filename = path

    def encode(self): 
        with sr.AudioFile(self.filename) as source:
            recorded_audio = self.r.listen(source)
            print("Done encoding")

        try:
            print("Recognizing text")
            self.audio_text = self.r.recognize_google(recorded_audio, language = 'en', show_all = True)
            output = open(r'Output.txt', 'w')
            output.write(print(self.audio_text["alternative"][0]["transcript"]))
            #with open('Output.txt', 'w') as f:
            #    f.write('' + self.audio_text)
            #    #f.write('end')
            #    f.close()
            #output = open(r'Output.txt', 'w')
            #output.write(self.audio_text)
            output.close()
            
        except:
            print('This failed!')
            
if __name__ == '__main__':
    main()
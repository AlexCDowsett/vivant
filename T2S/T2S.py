from _typeshed import Self
from gtts import gTTS
from playsound import playsound

import os

class T2S:
    def __init__(self, text):
        self.language = 'en'
        self.text = text
    
    def encode(self):
        speechObj = gTTS(text=self.text, lang=self.language, slow=False)
        
        #change this save desitination
        speechObj.save("speech.mp3")
    
    def play(self):
        #play the mps file
        playsound('speech.mp3')
        #os.system("afplay test.mp3")
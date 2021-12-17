#from _typeshed import Self
from gtts import gTTS
import os

def main():
    t2s = T2S("test")
    t2s.encode()
    t2s.play()
    t2s.remove()

class T2S:
    def __init__(self, text):
        self.language = 'en'
        self.text = text
        self.path = "speech.mp3"
    
    def encode(self):
        speechObj = gTTS(text=self.text, lang=self.language, slow=False)
        speechObj.save(self.path)
    
    def play(self):
        #play the mp3 file
        os.system("mpg123 " + self.path)

    def remove(self):
        os.system("sudo rm " + self.path)

if __name__ == '__main__':
    main()
    
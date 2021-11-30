from gtts import gTTS
from playsound import playsound

import os

language = 'en'

mytext = 'Hello World'

speechObj = gTTS(text=mytext, lang=language, slow=False)

speechObj.save("test.mp3")

#play the mps file
playsound('test.mp3')
#os.system("afplay test.mp3")
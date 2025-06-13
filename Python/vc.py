import webbrowser
import time
import os
import sys
import subprocess
from subprocess import DEVNULL, STDOUT
from pynput.keyboard import Key, Controller

def main():
    vc = VideoCall(None)
    time.sleep(8)
    vc.enter()
    time.sleep(30)

class VideoCall():
    def __init__(self, uuid):
        os.system("pkill chromium")
        url = "https://meet.jit.si/" + str(uuid) + "#config.startWithAudioMuted=false&config.startWithVideoMuted=false&config.prejoinPageEnabled=false&config.hideShareAudioHelper=true"
        subprocess.Popen(["chromium-browser", "--start-fullscreen", url], stdout=DEVNULL, stderr=STDOUT)

    def enter(self):
        self.keyboard = Controller()
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def __del__(self):
        os.system("pkill chromium")

        
if __name__ == '__main__':
    main()

#############
# User Parameters
#############

JITSI_ID = None  # If None, the program generates a random UUID
# JITSI_ID = "hackershackdoorbellexample"

import time
import os
import signal
import subprocess
import smtplib
import uuid

def main():
    chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
    video_chat = VideoChat(chat_id)
    video_chat.start()
    time.sleep(5)
    video_chat.end()
    print("fuck off")

class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return "http://meet.jit.si/%s#config.startWithVideoMuted=true" % self.chat_id

    def start(self):
        if not self._process and self.chat_id:
            #self.pid = os.fork()
            self._process = subprocess.Popen(["chromium-browser", "-kiosk", self.get_chat_url()])
        else:
            print("Can't start video chat -- already started or missing chat id")

    def end(self):
        if self._process:
            #os.kill(self._process.pid, signal.SIGTERM)
            #os.kill(self.pid, signal.SIGTERM)
            os.system("pkill -o chromium")
class Doorbell:
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin

    def run(self):
        try:
            print("Starting Doorbell...")
            hide_screen()
            self._setup_gpio()
            print("Waiting for doorbell rings...")
            self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")



if __name__ == "__main__":
    main()
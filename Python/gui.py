# MODULE IMPORTS
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import time
import os

# LOCAL IMPORTS
from time import sleep
from sql import Door
from sql import log
from fingerprint import Fingerprint
from fr import Camera
from fr import FaceReq
from vc import VideoCall

user = "alexd22"

# CONFIG
DEBUG_MODE = False
SETUP_MODE = False
BLUETOOTH = False
SCHEDULER_SPEED = 1000 # frequency of scheduler in miliseconds.
BG_COLOUR = '#FFFFFF' # Blackground colour in hexadecimal.                            
TEXT_COLOUR = '#343038' # Text colour in hexadecimal.
SC_WIDTH = 640
SC_HEIGHT = 480
PHOTOS_TO_TRAIN = 10
HEADER_FONT = 'Helvetica' # A font to be used primarily.
HEADER_FONT_SIZE = 36
BODY_FONT = 'Arial' # A font to be used secondarily.
BODY_FONT_SIZE = 24


def main():
    '''This function is run when the program starts.'''
    app = App(SETUP_MODE) # Creates an instance of the class Login with the tkinter window 'root' as a parameter.


class App():
        def __init__(self, setup=False):
            self.root = tk.Tk()
            self.root.title('Vivant GUI')
            self.root.geometry(str(SC_WIDTH) + 'x' + str(SC_HEIGHT))
            self.root.config(bg=BG_COLOUR)
            
            if DEBUG_MODE == False:
                self.root.focus_set()
                self.root.overrideredirect(True)
                self.root.wm_attributes("-topmost", 1)

            self.fp = False
            self.check_face = True
            self.fp_timer = 0
            self.ring_status = 0
            self.tts_status = False
            self.i = 0
            self.wrong_attempts = 0
                
            self.header_label = tk.Label(self.root, bg=BG_COLOUR, fg=TEXT_COLOUR, font=(HEADER_FONT, HEADER_FONT_SIZE, "bold"))
            self.header_label.place(x=0, y=20, w=SC_WIDTH, h=40)

            self.body_label = tk.Label(self.root, bg=BG_COLOUR, fg=TEXT_COLOUR, font=(BODY_FONT, BODY_FONT_SIZE))
            self.body_label.place(x=0, y=60, w=SC_WIDTH, h=(SC_HEIGHT-120))

            self.logo_image = tk.PhotoImage(file='resources/vivant-name-small.png')
            self.logo_label = tk.Label(self.root, image=self.logo_image)
            self.logo_label.place(x=((SC_WIDTH-320)/2),y=(SC_HEIGHT-60),w=320,h=51)
            self.logo_label.image = self.logo_image

            self.header_label.config(text="Welcome")
            self.body_label.config(text="\n\n\n\n\n\n\nPlease present your finger\non the scanner below")
            self.ring_gif = [tk.PhotoImage(file='resources/ring2.gif', format = 'gif -index %i' %(i)) for i in range(121)]
            self.ring_label = tk.Label(self.root, image=self.ring_gif[0], bg=BG_COLOUR)
            self.ring_label.place(x=((SC_WIDTH-250)/2), y=80, w=250, h=250)
            self.ring_label.image = self.ring_gif[0]
            self.ring_label.bind('<Button-1>', self.ring)

            self.bell_image = tk.PhotoImage(file='resources/bell2.png')
            self.bell_label = tk.Label(self.root, image=self.bell_image, bg=BG_COLOUR)
            self.bell_label.place(x=((SC_WIDTH-100)/2), y=155, w=100, h=100)
            self.bell_label.image = self.bell_image
            self.bell_label.bind('<Button-1>', self.ring)

            self.cross_image = tk.PhotoImage(file='resources/red-cross2.png')
            self.tick_image = tk.PhotoImage(file='resources/green-tick2.png')

            bg_rgb = BG_COLOUR.lstrip('#')
            bg_rgb = tuple(int(bg_rgb[i:i + 2], 16) for i in range(0, 6, 2))

            text_rgb = TEXT_COLOUR.lstrip('#')
            text_rgb = tuple(int(text_rgb[i:i + 2], 16) for i in range(0, 6, 2))

            self.text_fade = []
            j = 0
            for j in range(121):
                self.text_fade.append('#%02x%02x%02x' % (round((text_rgb[0]*j/121)+(bg_rgb[0]*(120-j)/121)),round((text_rgb[1]*j/121)+(bg_rgb[1]*(120-j)/121)),round((text_rgb[2]*j/121)+(bg_rgb[2]*(120-j)/121))))

            self.door = Door(BLUETOOTH)
            if setup == True or self.door.setup_required == True:
                self.setup()
            else:
                self.setup = 0
                self.facereq = FaceReq()



            self.fingerprint = Fingerprint(self.door.users())
            self.scheduler()
            self.root.mainloop()

        def setup(self):
            self.setup = 1
            self.header_label.config(text="SETUP MODE")
            self.temp_label = tk.Label(self.root, bg=BG_COLOUR, fg=TEXT_COLOUR, font=(BODY_FONT, BODY_FONT_SIZE))
            self.temp_label.config(text="Please present your finger\non the scanner below\nto register your fingerprint.")
            self.temp_label.place(x=0, y=60, w=SC_WIDTH, h=(SC_HEIGHT-120))
            
        def ring(self, *args):
            if self.setup == 0:
                self.door.ring()
                self.ring_status = 1
                self.bell_label.bind('<Button-1>', '')
                self.ring_label.bind('<Button-1>', '')
                self.check_face = False
                del self.facereq
                self.videocall = VideoCall(self.door.uuid)



        def play_gif(self, i=0):
            if i == 0:
                self.bell_label.destroy()
            elif i < 120:
                self.ring_label.config(image=self.ring_gif[i])
                self.ring_label.image = self.ring_gif[i]
                self.body_label.config(fg=self.text_fade[120-i])
            elif i == 121:
                self.ring_label.destroy()
                self.ring_status = 2
                self.play_ringing_animation()
            elif i < 181:
                self.body_label.config(fg=self.text_fade[2*(i-120)])
            else:
                return
            
            i += 1
            self.root.after(10, self.play_gif, i)

        def play_ringing_animation(self):
            i = self.i%4
            if i == 0:
                self.body_label.config(text="Ringing   \n\nPlease wait")
            elif i == 1:
                self.body_label.config(text="Ringing.  \n\nPlease wait")
            elif i == 2:
                self.body_label.config(text="Ringing.. \n\nPlease wait")
            else:
                self.body_label.config(text="Ringing...\n\nPlease wait")

        def check(self):
            if self.fp == False:
                self.setup = 0
                if self.ring_status == 0:
                    self.ring_label.config(image=self.ring_gif[0])
                    self.ring_label.image = self.ring_gif[0]

                    self.bell_label = tk.Label(self.root, image=self.bell_image, bg=BG_COLOUR)
                    self.bell_label.place(x=((SC_WIDTH-100)/2), y=155, w=100, h=100)
                    self.bell_label.image = self.bell_image
                    self.body_label.config(text="\n\n\n\n\n\n\nPlease present your finger\non the scanner below")
                    self.bell_label.bind('<Button-1>', self.ring)
                                    
                return
            
            self.setup = -1
            self.bell_label.destroy()
            if self.fp == True:
                log("No match found!")
                self.fp_timer = 3
                if self.ring_status == 0:
                    self.ring_label.config(image=self.cross_image)
                    self.ring_label.image = self.cross_image
                    self.body_label.config(text="\n\n\n\n\n\n\nAccess denied.\nPlease try again.")
                    
                    self.wrong_attempts += 1
                    if self.wrong_attempts >= 5:
                        self.wrong_attempts = 0
                        self.fp_timer = 60
                        self.body_label.config(text="\n\n\n\n\n\n\nMaximum attempts exceeded.\nPlease try again later.")
            else:
                self.fp_timer = 10
                if self.fp[1] == None:
                    log("Facial recognition found for " + self.fp[0] + '.')
                else:
                    log("Fingerprint found for " + self.fp[0] + " with an accuracy score of " + str(self.fp[1]) + '.')
                self.door.unlock()
                if self.ring_status == 0:
                    self.ring_label.config(image=self.tick_image)
                    self.ring_label.image = self.tick_image
                    self.body_label.config(text="\n\n\n\n\n\n\nAccess granted.\nWelcome " + self.door.name_of_user(self.fp[0])[0] + '.')
                    
        def picture(self, event):
            self.setup = 6
            self.camera=True
            self.pictures_saved = 0
            self.temp_label.bind('<Button-1>', '')
            self.temp2_label.destroy()
            self.picture_timer = 5
            self.cam = Camera(user)
            self.cam_label = tk.Label(self.root, bg=BG_COLOUR)
            self.cam_label.place(x=0, y=0, w=SC_WIDTH, h=SC_HEIGHT)
            self.countdown_label = tk.Label(bg=BG_COLOUR, fg=TEXT_COLOUR, text=str(self.picture_timer), font=(HEADER_FONT, 80, "bold"))
            self.countdown_label.place(x=0, y=0, w=70, h=90)
            self.num_label = tk.Label(bg=BG_COLOUR, fg=TEXT_COLOUR, text=("1/"+str(PHOTOS_TO_TRAIN)), font=(HEADER_FONT, 36, "bold"))
            self.num_label.place(x=(SC_WIDTH-120), y=0, w=120, h=50)
            self.camera_update()

        def camera_update(self):
            if self.camera == True:
                cam_image = ImageTk.PhotoImage(image=Image.fromarray(self.cam.update()))
                self.cam_label.config(image=cam_image)
                self.cam_label.image = cam_image
                self.root.after(33, self.camera_update)
            

        def scheduler(self):
            result = True
            while result == True:
                result = self.door.check()
                if (result != True) and (result != False):
                    self.tts_message = result
                    #result = '\n'.join(result[i:i+40] for i in range(0, len(result), 40))
                    
                    i = 0
                    j = 0
                    result = list(result)
                    for i in range(0, len(result)):
                        j += 1
                        if (result[i] == ' ') and j >= 40:
                            result.insert(i, '\n')
                            j = 0
                    result = ''.join(result)
                    
                    self.tts_label = tk.Label(self.root, bg=BG_COLOUR, fg=TEXT_COLOUR, font=(BODY_FONT, BODY_FONT_SIZE))
                    self.tts_label.config(text=("Message recieved from owner:\n" + result))
                    self.tts_label.place(x=0, y=60, w=SC_WIDTH, h=(SC_HEIGHT-120))
                    self.tts_status = True
                    self.tts_timer = self.i + 2
                    
            if (self.tts_status == True) and (self.tts_timer < self.i):
                self.door.tts_play(self.tts_message)
                self.tts_label.destroy()
                self.tts_status = False

            if self.ring_status == 1:
                self.ring_status = 0
                self.play_gif()
                self.ring_timer = self.i + 5
                #chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
                #video_chat = VideoChat(chat_id)
                #video_chat.start()

            if self.ring_status == 2:
                self.play_ringing_animation()
                if self.ring_timer == self.i:
                    self.root.withdraw()
                    
                if self.ring_timer < (self.i - 60):
                    self.root.deiconify()
                    del self.videocall
                    self.body_label.config(text="Call ended.")
                    self.ring_status = 3
                    
            elif self.ring_status == 3 and (self.ring_timer < (self.i - 62)):
                self.facereq = FaceReq()
                self.check_face = True
                    
                self.body_label.config(text="\n\n\n\n\n\n\nPlease present your finger\non the scanner below")
                self.ring_label = tk.Label(self.root, image=self.ring_gif[0], bg=BG_COLOUR)
                self.ring_label.place(x=((SC_WIDTH-250)/2), y=80, w=250, h=250)
                self.ring_label.image = self.ring_gif[0]
                self.ring_label.bind('<Button-1>', self.ring)

                self.bell_label = tk.Label(self.root, image=self.bell_image, bg=BG_COLOUR)
                self.bell_label.place(x=((SC_WIDTH-100)/2), y=155, w=100, h=100)
                self.bell_label.image = self.bell_image
                self.bell_label.bind('<Button-1>', self.ring)
                    
                self.ring_status = 0
                
            if self.setup == 1:
                result = self.fingerprint.enroll()
                if result == True:
                    self.setup = 3
                    log("Fingerprint scanned.")
                    self.temp_label.config(text="Fingerprint scanned.\nPlease remove your finger.")
                    
                elif result != False:
                    log("Fingerprint already exists for user " + result + '.')
                    self.setup = 2
                    name = self.door.name_of_user(result)
                    name = name[0] + ' ' + name[1]
                    self.temp_label.config(text="Fingerprint already registered\nfor " + name + ".\nPlease try a different finger.")
                    
            if self.setup == 2:
                if self.fingerprint.is_finger_present() == False:
                    self.setup = 1
                    self.temp_label.config(text="Please present your finger\non the scanner below\nto register your fingerprint.")

                    
            if self.setup == 3:
                if self.fingerprint.is_finger_present() == False:
                    self.setup = 4
                    self.temp_label.config(text="Please present your finger\non the scanner below\nagain.")

                    
            if self.setup == 4:
                result = self.fingerprint.enroll_confirm(user)
                if result == True:
                    self.setup = 2
                    log("Fingerprints do not match.")
                    self.temp_label.config(text="Fingerprints do not match.\nPlease try again.")
                elif result != False:
                    log("Fingerprint registered sucessfully for user " + user + '.')
                    self.temp_label.config(text="Fingerprint successfully registered.\nYou now have access to your\nVivant Security System.")
                    self.setup = 5
                    
            if self.setup == 5:
                self.temp_label.config(text="Now to learn your face. Please stand in\nfront of the camera and 10 photos will\nbe taken. Change the angle of your face\nslightly after every photo.\n\n")
                self.temp2_label = tk.Label(self.root, bg=BG_COLOUR, fg=TEXT_COLOUR, text="Press the screen when you are ready.", font=(BODY_FONT, BODY_FONT_SIZE, 'bold'))
                self.temp2_label.place(x=0, y=280, w=SC_WIDTH, h=40)
                self.temp_label.bind('<Button-1>', self.picture)
                self.temp2_label.bind('<Button-1>', self.picture)
                    
            if self.setup == 6:
                if self.camera == False:
                    if self.pictures_saved >= PHOTOS_TO_TRAIN:
                        self.countdown_label.destroy()
                        self.num_label.destroy()
                        self.cam_label.destroy()
                        self.temp2_label.destroy()
                        self.temp_label.config(text='Setup complete.\nTraining data, please wait...')
                        self.setup = 7
                        
                    else:
                        self.picture_timer = 3
                        self.num_label.config(text=str(self.pictures_saved+1) + '/' + str(PHOTOS_TO_TRAIN))
                        self.countdown_label.config(text=str(self.picture_timer))
                        self.camera = True
                        self.camera_update()
                    
                    
                elif self.picture_timer > 0:
                    self.picture_timer -= 1
                    self.countdown_label.config(text=str(self.picture_timer))
                    
                elif self.picture_timer == 0:
                    self.cam.save()
                    self.camera = False
                    self.pictures_saved += 1
                    
            elif self.setup == 7:
                self.cam.train(True)
                del self.cam
                self.facereq = FaceReq()
                name = self.door.name_of_user(user)
                log(name[0] + ' ' + name[1] + "'s fingerprints and face added to system.")
                self.setup = 8
                
            if self.setup == 8:
                if self.fingerprint.is_finger_present() == False:
                    self.setup = 0
                    self.header_label.config(text='Welcome')
                    self.temp_label.destroy()
                    
            if self.setup == 0:
                if self.check_face == True:
                    self.face = self.facereq.search()
                    if self.face != None:
                        self.fp = [self.face, None]
                        self.check()
                    
                self.fp = self.fingerprint.search()
                if self.fp != False:
                    self.check()



            if self.setup == -1:
                self.fp_timer -= 1
                
                if self.fp_timer <= 0:
                    self.fp = False
                    self.face = None
                    self.check()
            
            self.i += 1
            self.root.after(SCHEDULER_SPEED, self.scheduler)

        
                
                

if __name__ == '__main__':
    main()

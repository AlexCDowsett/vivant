import tkinter as tk
from time import sleep
from sql import Door
from sql import log
from fingerprint import Fingerprint

user = "alexd22"
known = False

# CONFIG
debug_mode = True
setup_mode = True
scheduler_speed = 1000 # frequency of scheduler in miliseconds.
bg_colour = '#FFFFFF' # Blackground colour in hexadecimal.                            
text_colour = '#343038' # Text colour in hexadecimal.                             
                              
header_font = 'Helvetica' # A font to be used primarily.
header_font_size = 22
body_font = 'Arial' # A font to be used secondarily.
body_font_size = 18


def main():
    '''This function is run when the program starts.'''
    app = App(setup_mode) # Creates an instance of the class Login with the tkinter window 'root' as a parameter.


class App():
        def __init__(self, setup=False):
            self.root = tk.Tk()
            self.root.title('Vivant GUI')
            self.root.geometry('480x320')
            self.root.resizable(False,False)
            self.root.config(bg=bg_colour)
            
            if debug_mode == False:
                self.root.focus_set()
                self.root.overrideredirect(True)
                self.root.wm_attributes("-topmost", 1)
                
            if setup == True:
                self.setup = 1
            else:
                self.setup = 0

            self.fp = False
            self.fp_timer = 0
            self.ring_status = 0
            self.i = 0
                
            self.header_label = tk.Label(self.root, bg=bg_colour, fg=text_colour, font=(header_font, header_font_size, "bold"))
            self.header_label.place(x=0, y=10, w=480, h=30)

            self.body_label = tk.Label(self.root, bg=bg_colour, fg=text_colour, font=(body_font, body_font_size))
            self.body_label.place(x=0, y=40, w=480, h=220)

            self.logo_image = tk.PhotoImage(file='resources/vivant-name-small.png')
            self.logo_label = tk.Label(self.root, image=self.logo_image)
            self.logo_label.place(x=80,y=265,w=320,h=51)
            self.logo_label.image = self.logo_image

            if known == True:
                self.header_label.config(text="Welcome back " + user)
                self.body_label.config(text="\nPlease present your finger\n on the scanner below")
            else:
                self.header_label.config(text="Welcome")
                self.body_label.config(text="\n\n\n\n\n\nPlease present your finger\non the scanner below")
                self.ring_gif = [tk.PhotoImage(file='resources/ring.gif', format = 'gif -index %i' %(i)) for i in range(121)]
                self.ring_label = tk.Label(self.root, image=self.ring_gif[0], bg=bg_colour)
                self.ring_label.place(x=165, y=50, w=150, h=150)
                self.ring_label.image = self.ring_gif[0]
                self.ring_label.bind('<Button-1>', self.ring)

                self.bell_image = tk.PhotoImage(file='resources/bell.png')
                self.bell_label = tk.Label(self.root, image=self.bell_image, bg=bg_colour)
                self.bell_label.place(x=215, y=100, w=50, h=50)
                self.bell_label.image = self.bell_image
                self.bell_label.bind('<Button-1>', self.ring)

                self.cross_image = tk.PhotoImage(file='resources/red-cross.png')
                self.tick_image = tk.PhotoImage(file='resources/green-tick.png')

                bg_rgb = bg_colour.lstrip('#')
                bg_rgb = tuple(int(bg_rgb[i:i + 2], 16) for i in range(0, 6, 2))

                text_rgb = text_colour.lstrip('#')
                text_rgb = tuple(int(text_rgb[i:i + 2], 16) for i in range(0, 6, 2))

                self.text_fade = []
                j = 0
                for j in range(121):
                        self.text_fade.append('#%02x%02x%02x' % (round((text_rgb[0]*j/121)+(bg_rgb[0]*(120-j)/121)),round((text_rgb[1]*j/121)+(bg_rgb[1]*(120-j)/121)),round((text_rgb[2]*j/121)+(bg_rgb[2]*(120-j)/121))))

            if self.setup == 1:
                self.header_label.config(text="SETUP MODE")
                self.temp_label = tk.Label(self.root, bg=bg_colour, fg=text_colour, font=(body_font, body_font_size))
                self.temp_label.config(text="Please present your finger\non the scanner below\nto register your fingerprint.")
                self.temp_label.place(x=0, y=40, w=480, h=220)
                
            self.door = Door()
            self.fingerprint = Fingerprint(self.door.users())
            self.scheduler()
            self.root.mainloop()

        def ring(self, *args):
            if self.setup == 0:
                self.door.ring()
                self.ring_status = 1
                self.bell_label.bind('<Button-1>', '')
                self.ring_label.bind('<Button-1>', '')

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

        def fp_check(self):
            if self.fp == False:
                self.setup = 0
                if self.ring_status == 0:
                    self.ring_label.config(image=self.ring_gif[0])
                    self.ring_label.image = self.ring_gif[0]

                    self.bell_label = tk.Label(self.root, image=self.bell_image, bg=bg_colour)
                    self.bell_label.place(x=215, y=100, w=50, h=50)
                    self.bell_label.image = self.bell_image
                    self.body_label.config(text="\n\n\n\n\n\nPlease present your finger\n on the scanner below")
                                    
                return
            
            self.setup = -1
            self.bell_label.destroy()
            if self.fp == True:
                log("No match found!")
                if self.ring_status == 0:
                    self.ring_label.config(image=self.cross_image)
                    self.ring_label.image = self.cross_image
                    self.body_label.config(text="\n\n\n\n\n\nAccess denied.\nPlease try again.")
            else:
                log("Fingerprint found for " + self.fp[0] + " with an accuracy score of " + str(self.fp[1]) + '.')
                self.door.unlock()
                if self.ring_status == 0:
                    self.ring_label.config(image=self.tick_image)
                    self.ring_label.image = self.tick_image
                    self.body_label.config(text="\n\n\n\n\n\nAccess granted.\nWelcome " + self.door.name_of_user(self.fp[0])[0] + '.')
                

        def scheduler(self):
            while self.door.check():
                ''

            if self.ring_status == 1:
                self.ring_status = 0
                self.play_gif()

            if self.ring_status == 2:
                self.play_ringing_animation()
                
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
                if self.fingerprint.is_finger_present() == False:
                    self.setup = 0
                    self.header_label.config(text='Welcome')
                    self.temp_label.destroy()
            if self.setup == 0:

                self.fp = self.fingerprint.search()
                if self.fp != False:
                    self.fp_timer = 3
                    self.fp_check()



            if self.setup == -1:
                self.fp_timer -= 1
                
                if self.fp_timer <= 0:
                    self.fp = False
                    self.fp_check()
            
            self.i += 1
            self.root.after(scheduler_speed, self.scheduler)

        
                
                

if __name__ == '__main__':
    main()

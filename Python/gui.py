import tkinter as tk
from time import sleep
from sql import Door

user = "Chris"
known = False

# CONFIG
debug = True
scheduler_speed = 1000 # frequency of scheduler in miliseconds.

bg_colour = '#FFFFFF' # Blackground colour in hexadecimal.                            
text_colour = '#343038' # Text colour in hexadecimal.                             
                              
header_font = 'Helvetica' # A font to be used primarily.
header_font_size = 22
body_font = 'Arial' # A font to be used secondarily.
body_font_size = 18


def main():
    '''This function is run when the program starts.'''
    app = App() # Creates an instance of the class Login with the tkinter window 'root' as a parameter.


class App():
        def __init__(self):
            self.root = tk.Tk()
            self.root.title('Vivant GUI')
            self.root.geometry('480x320')
            self.root.resizable(False,False)
            self.root.config(bg=bg_colour)
            
            if debug == False:
                self.root.focus_set()
                self.root.overrideredirect(True)
                self.root.wm_attributes("-topmost", 1)
                
            self.header_label = tk.Label(self.root, bg=bg_colour, fg=text_colour, font=(header_font, header_font_size, "bold"))
            self.header_label.place(x=0, y=20, w=480, h=60)

            self.body_label = tk.Label(self.root, bg=bg_colour, fg=text_colour, font=(body_font, body_font_size))
            self.body_label.place(x=0, y=90, w=480, h=140)

            self.logo_image = tk.PhotoImage(file='resources/vivant-name-small.png')
            self.logo_label = tk.Label(self.root, image=self.logo_image)
            self.logo_label.place(x=80,y=260,w=320,h=51)
            self.logo_label.image = self.logo_image

            if known == True:
                self.header_label.config(text="Welcome back " + user)
                self.body_label.config(text="Please present your finger\n on the scanner below")
            else:
                self.header_label.config(text="Welcome")
                self.ring_gif = [tk.PhotoImage(file='resources/ring.gif', format = 'gif -index %i' %(i)) for i in range(121)]
                self.ring_label = tk.Label(self.root, image=self.ring_gif[0], bg=bg_colour)
                self.ring_label.place(x=165, y=90, w=150, h=150)
                self.ring_label.image = self.ring_gif[0]
                self.ring_label.bind('<Button-1>', self.ring)

                self.bell_image = tk.PhotoImage(file='resources/bell.png')
                self.bell_label = tk.Label(self.root, image=self.bell_image, bg=bg_colour)
                self.bell_label.place(x=215, y=140, w=50, h=50)
                self.bell_label.image = self.bell_image
                self.bell_label.bind('<Button-1>', self.ring)

                bg_rgb = bg_colour.lstrip('#')
                bg_rgb = tuple(int(bg_rgb[i:i + 2], 16) for i in range(0, 6, 2))

                text_rgb = text_colour.lstrip('#')
                text_rgb = tuple(int(text_rgb[i:i + 2], 16) for i in range(0, 6, 2))

                self.text_fade = []
                j = 0
                for j in range(30):
                        self.text_fade.append('#%02x%02x%02x' % (round((text_rgb[0]*j/30)+(bg_rgb[0]*(30-j)/30)),round((text_rgb[1]*j/30)+(bg_rgb[1]*(30-j)/30)),round((text_rgb[2]*j/30)+(bg_rgb[2]*(30-j)/30))))

            self.door = Door()
            self.scheduler()
            self.root.mainloop()

        def ring(self, *args):
            self.door.ring()
            self.ring = 1

        def play_gif(self, i=0):
            if i == 0:
                self.bell_label.destroy()
            elif i < 121:
                self.ring_label.config(image=self.ring_gif[i])
                self.ring_label.image = self.ring_gif[i]
            elif i == 121:
                self.ring_label.destroy()
            elif i < 152:
                self.body_label.config(text="Ringing   \n\nPlease wait", fg=self.text_fade[i-122])
            else:
                self.ring = 2
                return
            
            i += 1
            self.root.after(10, self.play_gif, i)

        def play_ringing_animation(self, i=0):
            if i == 0:
                self.body_label.config(text="Ringing   \n\nPlease wait")
            elif i == 1:
                self.body_label.config(text="Ringing.  \n\nPlease wait")
            elif i == 2:
                self.body_label.config(text="Ringing.. \n\nPlease wait")
            else:
                self.body_label.config(text="Ringing...\n\nPlease wait")

        def scheduler(self, i=0):
            while self.door.check():
                ''

            if self.ring == 1:
                self.play_gif()
                self.ring = 2

            if self.ring == 2:
                self.play_ringing_animation(i%4)
                
            i += 1
            self.root.after(scheduler_speed, self.scheduler, i)

        
                
                

if __name__ == '__main__':
    main()

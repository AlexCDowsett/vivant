
import tkinter as tk
from time import sleep
class App():

	#Attributes - Fields
	#Constructors
	def __init__(self):

		self.root = tk.Tk()
		
		self.root.title('GUI')
		self.root.geometry('480x320')
		self.root.resizable(False,False)
		self.root.config(bg='white')
		#self.root.attributes("-fullscreen", False)
		
##### SCENES ######
##### 1
		self.frame1_known = tk.Frame(self.root, bg = "green")
		self.frame1_known.place(x=0, y=0, w=480, h=320)
		self.frame1_unknown = tk.Frame(self.root, bg = "red")
		self.frame1_unknown.place(x=0, y=0, w=480, h=320)
		
		self.ring_button = tk.Button(self.frame1_unknown, text = "Ring Chime(s)", command = self.fncRing)
		self.ring_button.place(x=10, y=50, w=460, h=260)

##### 2

		self.frame2_ringing = tk.Frame(self.root, bg = "blue")
		self.frame2_ringing.place(x=0, y=0, w=480, h=320)

		self.ringing_label = tk.Label(self.frame2_ringing, text = "Ringing homeowner(s)")
		self.ringing_label.place
	
		self.frame2_fpfail = tk.Frame(self.root, bg = "yellow")		
		self.frame2_fpfail.place(x=0, y=0, w=480, h=320)
		


##### 3

		self.frame3a = tk.Frame(self.root, bg = "green")
		self.frame3b = tk.Frame(self.root, bg = "brown")

		self.lab1f1.place(x=0, y=0, w=480, h=40)		
		self.frame41 = tk.Frame(self.root, bg = "orange")
		self.lab1f1.place(x=0, y=0, w=480, h=40)
		self.frame5 = tk.Frame(self.root, bg = "pink")

		self.lab1f1.place(x=0, y=0, w=480, h=40)

		self.lab1f1.place(x=0, y=0, w=480, h=40)

		self.btn1to2.place(x=0, y=40, w=480, h=280)
		self.lab11f = tk.Label(self.frame11, text = "Welcome \n Please choose an option:")
		self.btn1to3.place(x=0, y=40, w=480, h=280)		self.lab12f = tk.Label(self.frame12, text = "Homeowners, please use the finger print scanner")
		self.lab12f.config(font=("Courier", 22))
		self.btn2to3.place(x=0, y=40, w=480, h=280)		self.lab13f = tk.Label(self.frame13, text = "Welcome Home " + str(testName))
		

		self.btn3to1.place(x=0, y=40, w=480, h=280)
			
		self.lab21f22 = tk.Label(self.frame22, text = "Sorry we couldn't contact a homeowner \n would you like to leave a message?")
		
		self.lab21f23 = tk.Label(self.frame23, text = "" + str(testName) + "is on the line")

		self.lab1f31 = tk.Label(self.frame31, text = "Finger print used incorrectly \n Please try again \n\n Attempts remaining " + str(attemptsRem))
		#If the person was recognised from the scanner use lab13f
		self.lab31f32 = tk.Label(self.frame32, text = "No attempts remaining. \n Please try to log in via the Vivant app \n or \n FUCK OFF")

		self.lab22f41 = tk.Label(self.frame41, text = "Would you like to retake your message?")
		
		self.lab5f = tk.Label(self.frame4, text = "Thank you \n\n Goodbye")


	###### buttons #####


		self.btn3toRLM = tk.Button(self.frame22, text = "Yes", command = self.fncRM)
		self.btn3toGB = tk.Button(self.frame22, text = "No", command =self.fncGB)




		self.frame1.pack()
		self.root.mainloop()

		testName = "Chris"
		attemptRem = 5;

	#Behaviours - Methods
	def fnc1to2(self):
		print("1 to 2")
		self.frame11.pack_forget()
		self.frame21.pack()

	def fnc1to3(self):
		print("1 to 3")
		self.frame1.pack_forget()
		self.frame3.pack()

	def fnc2to3(self):
		print("2 to 3")
		self.frame21.pack_forget()

	def fnc2to3(self):
		print("2 to 3")
		self.frame21.pack_forget()
		self.frame3.pack()

	def fncRM(self):
		print("Leaving recorded message")
		self.frame.pack_forget()
		self.frame1.pack()

	def fncGB(self):
		print("Goodbye")
		self.frame3b.pack_forget()
		self.frame5.pack()
		sleep(20)
		# if facial_recog returns face cut to the frame 12
		self.frame5.pack_forget()
		self.frame1a.pack()

a = App()

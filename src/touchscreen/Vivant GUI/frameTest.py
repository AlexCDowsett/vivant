
import tkinter as tk

class App():

	#Attributes - Fields
	#Constructors
	def __init__(self):

		self.root = tk.Tk()
		#enable this next line for the real thing.
		#self.root.attributes("-fullscreen", True)
##### frames ######
		self.frame11 = tk.Frame(self.root, bg = "red")
		self.frame12 = tk.Frame(self.root, gb = "red")
		self.frame21 = tk.Frame(self.root, bg = "blue")
		self.frame22 = tk.Frame(self.root, bg = "yellow")
		self.frame23 = tk.Frame(self.root, gb = "white")
		self.frame31 = tk.Frame(self.root, bg = "green")
		self.frame32 = tk.Frame(self.root, bg = "brown")
		self.frame41 = tk.Frame(self.root, bg = "orange")
		self.frame5 = tk.Frame(self.root, bg = "pink")

	###### labels ######
		self.lab11f = tk.Label(self.frame11, text = "Welcome \n Please choose an option:")
		self.lab12f = tk.Label(self.frame12, text = "Homeowners, please use the finger print scanner")
		self.lab12f.config(font=("Courier", 22))
		self.lab13f = tk.Label(self.frame13, text = "Welcome Home " + str(testName))
		

		self.lab1f21 = tk.Label(self.frame21, text = "Ringing homeowner(s)")
			
		self.lab21f22 = tk.Label(self.frame22, text = "Sorry we couldn't contact a homeowner \n would you like to:")
		
		self.lab21f23 = tk.Label(self.frame23, text = "" + str(testName) + "is on the line")

		self.lab1f31 = tk.Label(self.frame31, text = "Finger print used incorrectly \n Please try again \n\n Attempts remaining " + str(attemptsRem))
		#If the person was recognised from the scanner use lab13f
		self.lab31f32 = tk.Label(self.frame32, text = "No attempts remaining. \n Please try to log in via the Vivant app \n or \n FUCK OFF")

		self.lab1f41 = tk.Label(self.frame41, text = "Would you like to retake your message?")
		
		self.lab5f = tk.Label(self.frame4, text = "Thank you \n\n Goodbye")


	###### buttons #####

		self.btn1to2 = tk.Button(self.frame11, text = "Ring Chime(s)", command = self.fncRing)
		
		self.btn1to3 = tk.Button(self.frame11, text = "Leave a Message?", command = self.fncLM)

		#self.btn2toRing = tk.Button(self.frame21, text = "Ringing doorbell", command = self.fncRing)
		#self.btnRingtoAns = tk.Button(self.frame21, text = "X is on the Line", command = self.fncTalk)
		
		self.btnRingtoMiss = tk.Button(self.frame22, text = "Leave a voice message", command = self.fncLM)
		self.btnRingtoMiss = tk.Button(self.frame22, text = "Ring again", command = self.fncRing)

		self.btn2toLM = tk.Button(self.frame22, text = "Hold here to leave a message", command = self.fncLM)
		self.btn2toRLM = tk.Button(self.frame22, text = "Yes", command = )
		self.btn2toRLM = tk.Button(self.frame22, text = "No", command = )
		
		#self.btn3to1 = tk.Button(self.frame3, text = "Thank you \n Goodbye", command = self.fnc3to1)

		#frame 1
		self.lab1f1.pack()
		self.btn1to3.pack()
		self.btn1to2.pack()

		#frame 2
		self.lab1f21.pack()
		self.btn2to3.pack()

		#frame 3
		self.lab1f3.pack()
		self.btn3to1.pack()




		self.frame1.pack()
		self.root.mainloop()

		testName = "Chris"
		attemptRem = 5;

	#Behaviours - Methods
	def fnc1to2(self):
		print("1 to 2")
		self.frame1.pack_forget()
		self.frame21.pack()

	def fnc1to3(self):
		print("1 to 3")
		self.frame1.pack_forget()
		self.frame3.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

	def fnc2to3(self):
		print("2 to 3")
		self.frame21.pack_forget()
		self.frame3.pack()

	def fnc3to1(self):
		print("3 to 1")
		self.frame3.pack_forget()
		self.frame1.pack()


a = App()

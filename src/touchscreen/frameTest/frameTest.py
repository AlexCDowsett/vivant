
import tkinter as tk

class App():

	#Attributes - Fields
	#Constructors
	def __init__(self):

		self.root = tk.Tk()
		#enable this next line for the real thing.
		#self.root.attributes("-fullscreen", True)

		self.frame1 = tk.Frame(self.root, bg = "red")
		self.frame21 = tk.Frame(self.root, bg = "blue")
		self.frame22 = tk.Frame(self.root, bg = "yellow")
		self.frame3 = tk.Frame(self.root, bg = "green")

		self.lab1f1 = tk.Label(self.frame1, text = "Welcome")
		self.lab1f21 = tk.Label(self.frame21, text = "Second frame part 1")
		self.lab1f22 = tk.Label(self.frame22, text = "Second frame part 2")
		self.lab1f3 = tk.Label(self.frame3, text = "Frame 3")

		self.btn1to2 = tk.Button(self.frame1, text = "Ring Doorbell", command = self.fnc1to3)
		self.btn1to3 = tk.Button(self.frame1, text = "Leave message", command = self.fnc1to2)

		self.btn2to3 = tk.Button(self.frame21, text = "Ringing doorbell", command = self.fnc2to3)

		self.btn3to1 = tk.Button(self.frame3, text = "Thank you \n Goodbye", command = self.fnc3to1)

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

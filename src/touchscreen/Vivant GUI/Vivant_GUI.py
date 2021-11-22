import tkinter as tk



window = tk.Tk()

def toggle():
    print('Who is Joe?')

def toggleRet():
    print('Joe Mama')
    label1["state"] = "disabled"
    label2["state"] = "disabled"
    label3.pack(fill=tk.BOTH, expand=True)

label1 = tk.Button(
    text="Hello, World",
    foreground="blue",  # Set the text color to white
    background="black",  # Set the background color to black
    width=25,
    height=10,
    command = toggle
)

label2 = tk.Button(
    text="Second button",
    foreground="orange",  # Set the text color to white
    background="white",  # Set the background color to black
    width=25,
    height=10,
    command = toggleRet
)

label3 = tk.Button(
    text="Get Fucked",
    foreground="white",  # Set the text color to white
    background="black",  # Set the background color to black
    width=25,
    height=10,
    command = toggleRet
)

label1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
label2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

window.mainloop()

from tkinter import *
from tkinter import ttk

def on_button_click():
    button_clicked.set(True)

root = Tk()

button_clicked = BooleanVar()
button_clicked.set(False)

button = ttk.Button(root, text="Press Me", command=on_button_click)
button.pack()

# Wait until the button is clicked
root.wait_variable(button_clicked)

# Continue with the rest of the program after the button is clicked
print("Button was clicked")

root.mainloop()
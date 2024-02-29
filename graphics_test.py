from tkinter import *
from tkinter import ttk

def update_text():
    label.config(text=new_text_entry.get())

root = Tk()
mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0)

# Create a label with initial text
initial_text = "Initial Text"
label = ttk.Label(mainframe, text=initial_text)
label.grid(column=2, row=1, sticky=N)

# Entry to input new text
new_text_entry = ttk.Entry(mainframe)
new_text_entry.grid(column=2, row=2, sticky=N)

# Button to update text
update_button = ttk.Button(mainframe, text="Update Text", command=update_text)
update_button.grid(column=2, row=3, sticky=N)

root.mainloop()
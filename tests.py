from tkinter import *

def update_text():
    canvas.itemconfig(text_item, text="Updated Text")

root = Tk()
canvas = Canvas(root, width=200, height=300)
canvas.pack()

# Create text on the canvas
text_item = canvas.create_text(100, 50, text="Original Text", fill="black")
canvas.create_text(100, 150, text="new Text", fill="black")
# Create a button to update the text
update_button = Button(root, text="Update Text", command=update_text)
update_button.pack()

root.mainloop()

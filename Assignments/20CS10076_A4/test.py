from tkinter import *
from tkinter import filedialog

def fileClick(clicked):
    file = filedialog.askopenfilename(initialdir="/", title="Select file")


root = Tk()
root.title("Segmentation and Bounding Boxes")

Options = ["Segmentation", "Bounding-box"]
clicked = StringVar(root)
clicked.set(Options[0])

e = Entry(root, width=70)
e.grid(row=0, column=0)

filebutton = Button(root, text="Browse", command= lambda: fileClick(clicked))
filebutton.grid(row=0, column=1)
print(clicked.get())
dropbutton = OptionMenu(root, clicked, *Options)
dropbutton.grid(row=0, column=2)

root.mainloop()
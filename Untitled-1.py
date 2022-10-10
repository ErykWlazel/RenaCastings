
from tkinter import *
from tkinter.ttk import *


root = Tk()
root.title("GG")
root.resizable(False, False)

treev = Treeview(root)
treev.pack() 

for i in ('allaf', 'lesio', 'smalczyk', 'bohdan.js'):
    treev.insert('', 'end', text=i)

for i in treev.get_children():
    print(i)

treev.reattach('I001', '', 0)





root.mainloop()
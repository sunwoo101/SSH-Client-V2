import paramiko
from tkinter import Tk, Frame, Button, Grid, ttk, StringVar, Label

# Variables
width = 800
height = 600

name = ""
username = ""
host = ""
port = "22"
password = ""


### Functions ###
# Button
def button(width,height,row,column,text,command):
    frame = Frame(fToolbar,width=width,height=height)
    frame.grid_propagate(False)
    frame.grid(row=row,column=column)
    button = Button(frame,text=text,activeforeground="grey",command=command)
    button.grid(row=1,column=1,sticky="nsew")
    Grid.columnconfigure(frame, 1, weight=1)
    Grid.rowconfigure(frame, 1, weight=1)

# Connect ssh
def connect_ssh():
    sNotification.set("Connected SSH")

# Connect ftp
def connect_ftp():
    sNotification.set("Connected FTP")

# Load
def load():
    sNotification.set("Loaded")

# Save
def save():
    sNotification.set("Saved")

# Delete
def delete():
    sNotification.set("Deleted")


### Window setup ###
# Window
root = Tk()
root.title("Py SSH")
root.geometry(f"{width}x{height}+500+250")
root.resizable(width=False,height=False)


### Toolbar widgets ###
# Toolbar frame #
fToolbar = Frame(root,width=150,height=600,bg="grey")
fToolbar.grid_propagate(False)
fToolbar.grid(row=1,column=1)

# Connect ssh button
button(width=150,height=50,row=1,column=1,text="Connect SSH",command=connect_ssh)

# Connect ftp button
button(width=150,height=50,row=2,column=1,text="Connect FTP",command=connect_ftp)

# Separator frame
fSeparator = Frame(fToolbar,width=150,height=300,bg="black")
fSeparator.grid_propagate(False)
fSeparator.grid(row=3,column=1)

# Notification text
sNotification = StringVar()
fNotification = Frame(fToolbar,width=150,height=25,bg="grey")
fNotification.grid_propagate(False)
fNotification.grid(row=4,column=1)
tNotification = Label(fNotification,textvariable=sNotification,fg="red")
tNotification.grid(row=1,column=1,sticky="nsew")
Grid.columnconfigure(fNotification, 1, weight=1)
Grid.rowconfigure(fNotification, 1, weight=1)

# Combobox
fDropdown = Frame(fToolbar,width=150,height=25)
fDropdown.grid_propagate(False)
fDropdown.grid(row=5,column=1)
cValue = StringVar()
cLogins = ttk.Combobox(fDropdown,textvariable=cValue)
cLogins.grid(row=1,column=1,sticky="nsew")
Grid.columnconfigure(fDropdown, 1, weight=1)
Grid.rowconfigure(fDropdown, 1, weight=1)

# Load button
button(width=150,height=50,row=6,column=1,text="Load",command=load)

# Save button
button(width=150,height=50,row=7,column=1,text="Save",command=save)

# Delete button
button(width=150,height=50,row=8,column=1,text="Delete",command=delete)


### Tabs ###
# Tab frame #
fTabs = Frame(root,width=650,height=600,bg="blue")
fTabs.grid_propagate(False)
fTabs.grid(row=1,column=2)

# Tab list #
tabs = ttk.Notebook(fTabs)

# Tab 1
tab1 = Frame(tabs,width=596,height=538,bg="grey")


tab2 = Frame(tabs)
tabs.add(tab1,text="test")
tabs.add(tab2,text="test2")
tabs.grid(row=1,column=1)

root.mainloop()

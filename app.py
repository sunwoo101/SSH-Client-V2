import paramiko
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *


# Variables
width = 800
height = 600

name = ""
username = ""
host = ""
port = "22"
password = ""
connected_ssh = False



### Functions ###
# Button
def button(width, height, row, column, text, command, image=None):
    frame = Frame(fToolbar, width=width, height=height)
    frame.grid_propagate(False)
    frame.grid(row=row, column=column)

    button = Button(frame, text=text, activeforeground="grey", command=command, image=image, compound="left")
    button.grid(row=1, column=1, sticky="nsew")
    Grid.columnconfigure(frame, 1, weight=1)
    Grid.rowconfigure(frame, 1, weight=1)


# Connect ssh
def connect_ssh():
    global connected_ssh
    sNotification.set("Connected SSH")
    connected_ssh = True


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
    global connected_ssh
    sNotification.set("Deleted")
    connected_ssh = False


# Input
def input(event):
    global terminal_input, connected_ssh
    input = terminal_input.get()
    terminal_output.configure(state="normal")
    if connected_ssh:
        terminal_output.insert(INSERT, f"root@ubuntu: {input}\n")
    else:
        terminal_output.insert(INSERT, "No Connection\n")
    terminal_output.see(END)
    terminal_output.configure(state="disabled")
    terminal_input.delete(0, END)


### Window setup ###
# Window
root = Tk()
root.title("Remotre")
root.geometry(f"{width}x{height}+500+250")
root.resizable(width=False, height=False)

# Images
iSSH = PhotoImage(file = "./icons/ssh.png")
iFTP = PhotoImage(file = "./icons/ftp.png")
iLoad = PhotoImage(file = "./icons/load.png")
iSave = PhotoImage(file = "./icons/save.png")
iDelete = PhotoImage(file = "./icons/delete.png")

### Toolbar widgets ###
# Toolbar frame #
fToolbar = Frame(root, width=150, height=600, bg="grey")
fToolbar.grid_propagate(False)
fToolbar.grid(row=1, column=1)

# Connect ssh button
button(width=150, height=50, row=1, column=1, text="Connect SSH", command=connect_ssh, image=iSSH)

# Connect ftp button
button(width=150, height=50, row=2, column=1, text="Connect FTP", command=connect_ftp, image=iFTP)

# Selection frame
fSelection = Frame(fToolbar, width=150, height=225)
fSelection.grid_propagate(False)
fSelection.grid(row=3, column=1)

flSelection = Frame(fSelection, width=134, height=225)
flSelection.grid_propagate(False)
flSelection.grid(row=1, column=1)
lSelection = Listbox(flSelection)
lSelection.grid_propagate(False)
lSelection.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(flSelection, 1, weight=1)
Grid.rowconfigure(flSelection, 1, weight=1)

sSelection = Scrollbar(fSelection, orient="vertical")
sSelection.config(command=lSelection.yview)
sSelection.grid(row=1, column=2, sticky="nsew")
lSelection.config(yscrollcommand=sSelection.set)
Grid.columnconfigure(fSelection, 2, weight=1)

for x in range(100):
    lSelection.insert(END, f"Server {str(x+1)}")

# Notification text
sNotification = StringVar()
fNotification = Frame(fToolbar, width=150, height=25)
fNotification.grid_propagate(False)
fNotification.grid(row=4, column=1)
tNotification = Label(fNotification, textvariable=sNotification, fg="red")
tNotification.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(fNotification, 1, weight=1)
Grid.rowconfigure(fNotification, 1, weight=1)

# Entry frame #
fEntry = Frame(fToolbar, width=150, height=100, bg="grey")
fEntry.grid_propagate(False)
fEntry.grid(row=5, column=1)

# Username
Label(fEntry, text="Username:").grid(row=1, column=1, sticky=E)
eUsername = Entry(fEntry)
eUsername.grid(row=1, column=2)


# Load button
button(width=150, height=50, row=6, column=1, text="Load", command=load, image=iLoad)

# Save button
button(width=150, height=50, row=7, column=1, text="Save", command=save, image=iSave)

# Delete button
button(width=150, height=50, row=8, column=1, text="Delete", command=delete, image=iDelete)

### Tabs ###
# Tab frame #
fTabs = Frame(root, width=650, height=600, bg="blue")
fTabs.grid_propagate(False)
fTabs.grid(row=1, column=2)

# Tab list #
tabs = ttk.Notebook(fTabs)
tabs.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(fTabs, 1, weight=1)
Grid.rowconfigure(fTabs, 1, weight=1)

# SSH tab #
tSSH = Frame(tabs)
tabs.add(tSSH, text="SSH")

# Terminal output
terminal_output = ScrolledText(tSSH)
terminal_output.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(tSSH, 1, weight=1)
Grid.rowconfigure(tSSH, 1, weight=1)
terminal_output.configure(state="disabled")

# Terminal input
fTerminal_input = Frame(tSSH, bg="black")
fTerminal_input.grid(row=2, column=1, sticky="nsew")

terminal_input = Entry(fTerminal_input)
terminal_input.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(fTerminal_input, 1, weight=1)
Grid.rowconfigure(fTerminal_input, 1, weight=1)
terminal_input.bind('<Return>', input)


# FTP tab #
tFTP = Frame(tabs)
tabs.add(tFTP, text="FTP")


root.mainloop()

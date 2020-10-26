import platform
import os
import pickle
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk


# Variables
platform = platform.system()
username = ""
host = ""
port = "22"
login = ""

# Craete logins file if not already existing
if os.path.isfile("./logins.JSON") == False:
    pLogins = open("logins.JSON", "wb")
    logins = []
    pickle.dump(logins,pLogins)
    pLogins.close()

# Load list into variable
pLogins = open("logins.JSON","rb")
logins = []
logins = pickle.load(pLogins)
pLogins.close()


# Window setup
root = tk.Tk()
root.title("Python SSH Client")

fSelection = tk.Frame(root,padx=5,pady=5,bd=3,relief=tk.RIDGE)
fSelection.pack(side=tk.TOP,padx=10,pady=5)

fConnection = tk.Frame(root,padx=5,pady=5,bd=3,relief=tk.RIDGE)
fConnection.pack(side=tk.TOP,padx=10,pady=5)


# Connect function
def connect():
    username = eUsername.get()
    host = eHost.get()
    port = ePort.get()

    if platform == "Windows":
        tk.messagebox.showinfo(title="Connecting",message="Connecting... the connection window may start minimized")
        os.system(f"cmd /c start ssh {username}@{host} -p {port}")
    elif platform == "Darwin":
        tk.messagebox.showinfo(title="Connecting",message="Connecting... the connection window may start minimized")
        os.system(f"osascript -e 'tell app \"Terminal\"\n do script \"ssh {username}@{host} -p {port}\"\n end tell'")
    elif platform == "Linux":
        tk.messagebox.showinfo(title="Connecting",message="Connecting... the connection window may start minimized")
        os.system(f"gnome-terminal -e 'bash -c \"\"ssh {username}@{host} -p {port}\";bash\"'")
    else:
        tk.messagebox.showerror(title="Error",message="Your OS is not supported")


# Save function
def save():
    global login, username, host, port, logins

    login = eLogin.get()
    username = eUsername.get()
    host = eHost.get()
    port = ePort.get()

    # Load list into variable
    pLogins = open("logins.JSON","rb")
    logins = []
    logins = pickle.load(pLogins)
    pLogins.close()

    # Check if login name exists
    lLogins = []
    for i in logins:
        lLogins.append(i[0])
    
    if login in lLogins:
        tk.messagebox.showerror(title="Error",message="This login name already exists")
    elif login != "" and username != "" and host != "" and port != "":
        # Save to file
        logins.append([login,username,host,port])
        pLogins = open("logins.JSON","wb")
        pickle.dump(logins,pLogins)
        pLogins.close()

        refresh()
    else:
        tk.messagebox.showerror(title="Error",message="Entry/Entries are empty")


# Refresh function
def refresh():
    global login, username, host, port, logins, lLogins

    # Load list into variable
    pLogins = open("logins.JSON","rb")
    logins = []
    logins = pickle.load(pLogins)
    pLogins.close()

    # Load list into combobox
    cLogins['values'] = []
    lLogins = []
    for i in logins:
        lLogins.append(i[0])
        cLogins['values'] = lLogins

    # Clear entries
    eLogin.delete(0,tk.END)
    cLogins.delete(0,tk.END)


# Load function
def load():
    global login, username, host, port, logins

    lValue = cValue.get()
    a = 0
    l = []
    for i in lLogins:
        if str(lValue) == str(i):
            l = logins[a]
            username = l[1]
            host = l[2]
            port = l[3]

            eUsername.delete(0, tk.END)
            eUsername.insert(0, username)

            eHost.delete(0, tk.END)
            eHost.insert(0, host)

            ePort.delete(0, tk.END)
            ePort.insert(0, port)
        a += 1




# Delete function
def delete():
    global login, username, host, port, logins

    # Load list into variable
    pLogins = open("logins.JSON","rb")
    logins = []
    logins = pickle.load(pLogins)
    pLogins.close()

    lValue = cValue.get()
    a = 0
    for i in lLogins:
        if str(lValue) == str(i):
            delete = logins[a]
            logins.remove(delete)
        a += 1

    # Save to file
    pLogins = open("logins.JSON","wb")
    pickle.dump(logins,pLogins)
    pLogins.close()

    # Clear entries
    cLogins.delete(0,tk.END)


    refresh()


###################
# Selection frame #
###################

# Select login
tk.Label(fSelection, 
         text="Select:").grid(row=1, column=1, sticky=tk.E)

# Logins combobox
cValue = tk.StringVar()
cLogins = ttk.Combobox(fSelection,textvariable=cValue)
cLogins.grid(row=1,column=2)

# Load button
bLoad = tk.Button(fSelection, text ="Load", command = load)
bLoad.grid(row=1, column=3)

# Delete button
bLoad = tk.Button(fSelection, text ="Delete", command = delete)
bLoad.grid(row=1, column=4)

# Save login
tk.Label(fSelection, 
         text="Save as:").grid(row=2, column=1, sticky=tk.E)
eLogin = tk.Entry(fSelection)
eLogin.grid(row=2, column=2)
eLogin.insert(0, login)

# Save button
bSave = tk.Button(fSelection, text ="Save", command = save)
bSave.grid(row=2, column=3)

# Refresh button
bLoad = tk.Button(fSelection, text ="Refresh", command = refresh)
bLoad.grid(row=3, column=3)



####################
# Connection frame #
####################

# Username
tk.Label(fConnection, 
         text="Username:").grid(row=1, column=1, sticky=tk.E)
eUsername = tk.Entry(fConnection)
eUsername.grid(row=1, column=2)

# Host
tk.Label(fConnection, 
         text="Host:").grid(row=2, column=1, sticky=tk.E)
eHost = tk.Entry(fConnection)
eHost.grid(row=2, column=2)

# Port
tk.Label(fConnection, 
         text="Port:").grid(row=3, column=1, sticky=tk.E)
ePort = tk.Entry(fConnection)
ePort.grid(row=3, column=2)

# Connect button
bConnect = tk.Button(fConnection, text ="Connect", command = connect)
bConnect.grid(row=4, column=2)


refresh()


root.mainloop()

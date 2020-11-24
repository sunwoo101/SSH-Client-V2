from tkinter import *
from tkinter import ttk
from tkinter.font import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
import platform
import os
import pickle


### Login Screen ###
# Variables
logged = False

# Window
login = Tk()
login.title("Remotre - Login")
x_center = (login.winfo_screenwidth()/2) - 300
y_center = (login.winfo_screenheight()/2) - 200
login.geometry("+%d+%d" % (x_center, y_center))
login.resizable(width=False, height=False)

# Craete details file if not already existing
if os.path.isfile("./details.JSON") == False:
    details_file = open("details.JSON", "wb")
    details = []
    pickle.dump(details, details_file)
    details_file.close()

# Load list into variable
details_file = open("details.JSON", "rb")
details = []
details = pickle.load(details_file)
details_file.close()

user = details[0]
passwd = details[1]
plan = details[2]
days = details[3]

### Functions ###
# Loop
def loop():
    # Show or hide password
    if show_password_checkbox_variable.get() == 1:
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

    login.after(5, loop)


# Connect to database and login
def login_check(event=None):
    global logged, user, days, free_alert, basic_alert, premium_alert
    if password_entry.get() == "Password":
        # Save details
        logged = True
        user = username_entry.get()
        passwd = password_entry.get()
        if type(days) == "int":
            days -= 1
        details = [user, passwd, plan, days]
        details_file = open("details.JSON", "wb")
        pickle.dump(details, details_file)
        details_file.close()

        # Alert
        free_alert = f"[Remotre] Welcome {user}. You are currently using the free plan, upgrade to a paid plan to save connections to the cloud"
        basic_alert = f"[Remotre] Welcome {user}. You have {days} days remaining on your basic plan, upgrade to the premium plan to use the FTP tab"
        premium_alert = f"[Remotre] Welcome {user}. You have {days} days remaining on your premium plan"
        login.destroy()
    elif days < 1:
        login_error_string.set("Your plan has expired")
    else:
        login_error_string.set("Incorrect username/password")


# Frame
login_frame = Frame(login, relief="ridge", bd=10)
login_frame.grid(row=1, column=1, padx=150, pady=100)

# Label
login_string = StringVar()
login_label = Label(login_frame, textvariable=login_string)
login_label["font"] = Font(size=38)
login_string.set("Login")
login_label.grid(row=1, column=1, columnspan=2, sticky="nsew")

# Username
username_string = StringVar()
username_label = Label(login_frame, textvariable=username_string)
username_label["font"] = Font(size=12)
username_string.set("Username:")
username_label.grid(row=2, column=1, sticky="nsew")

username_entry = Entry(login_frame, bd=1)
username_entry.grid(row=2, column=2, sticky="nsew")
username_entry.insert(0, user)

# Password
password_string = StringVar()
password_label = Label(login_frame, textvariable=password_string)
password_label["font"] = Font(size=12)
password_string.set("Password:")
password_label.grid(row=3, column=1, sticky="nsew")

password_entry = Entry(login_frame, bd=1)
password_entry.grid(row=3, column=2, sticky="nsew")
password_entry.configure(show="*")
password_entry.insert(0, passwd)

show_password_checkbox_variable = IntVar()
show_password_checkbox = Checkbutton(login_frame, text="Show Password", variable=show_password_checkbox_variable)
show_password_checkbox.grid(row=4, column=1, columnspan=2)

# Button
login_button_frame = Frame(login_frame, width=50, height=20)
login_button_frame.grid_propagate(False)
Grid.columnconfigure(login_button_frame, 1, weight=1)
Grid.rowconfigure(login_button_frame, 1, weight=1)
login_button_frame.grid(row=5, column=1, columnspan=2)

login_button = Button(login_button_frame, text="Login", command=login_check)
login_button.grid(row=1, column=1, sticky="nsew")

login.bind("<Return>", login_check)

# Login error
login_error_string = StringVar()
login_error_label = Label(login_frame, fg="red", textvariable=login_error_string)
login_error_label["font"] = Font(size=12)
login_error_label.grid(row=6, column=1, columnspan=2, sticky="nsew")

loop()

login_frame.mainloop()

if logged == True:
    pass
else:
    exit()

### Main App ###
# Variables
width = 900
height = 670

name = ""
username = ""
hostname = ""
port = "22"
platform = platform.system()
RGB_variable = [235, 52, 52]

# Craete logins file if not already existing
if os.path.isfile("./logins.JSON") == False:
    logins_file = open("logins.JSON", "wb")
    logins = []
    pickle.dump(logins, logins_file)
    logins_file.close()

# Load list into variable
logins_file = open("logins.JSON", "rb")
logins = []
logins = pickle.load(logins_file)
logins_file.close()


### Functions ###
# Button
def button(frame, width, height, row, column, text, command, image=None):
    button_frame = Frame(frame, width=width, height=height)
    button_frame.grid_propagate(False)
    button_frame.grid(row=row, column=column)

    button = Button(button_frame, text=text, activeforeground="grey", command=command, image=image, compound="left", anchor=W)
    button.grid(row=1, column=1, sticky="nsew")
    Grid.columnconfigure(button_frame, 1, weight=1)
    Grid.rowconfigure(button_frame, 1, weight=1)


# Alert
def alert(text):
    alert_output.configure(state="normal")
    alert_output.insert(INSERT, text)
    alert_output.insert(INSERT, "\n")
    alert_output.see(END)
    alert_output.configure(state="disabled")


# Connect ssh
def connect_ssh():
    alert_output.configure(state="normal")

    name = name_entry.get()
    username = username_entry.get()
    hostname = hostname_entry.get()
    port = port_entry.get()

    # Set default port
    if type(port) != int:
        port = 22
    if port == "":
        port = 22

    try:
        # Mac
        if platform == "Darwin":
            os.system(f"osascript -e 'tell app \"Terminal\"\n do script \"ssh {username}@{hostname} -p {port}\"\n end tell'")
            alert(f"[Remotre] Connecting to '{name}' at '{username}@{hostname}:{port}' via ssh in a new terminal. Window may start minimized...")
        # Windows
        elif platform == "Windows":
            os.system(f"cmd /c start ssh {username}@{hostname} -p {port}")
            alert(f"[Remotre] Connecting to '{name}' at '{username}@{hostname}:{port}' via ssh in a new terminal...")
        # Linux
        elif platform == "Linux":
            """ this needs to be fixed
            os.system(f"gnome-terminal -e 'bash -c \"\"ssh {username}@{hostname} -p {port}\";bash\"'")
            """

            alert(f"[Remotre] Connecting to '{name}' at '{username}@{hostname}:{port}' via ssh in a new terminal...")
        else:
            alert(f"[Remotre] Sorry, your OS is not yet supported")
    except:
        print("Entries are invalid")
    alert_output.see(END)
    alert_output.configure(state="disabled")


# Connect ftp
def connect_ftp():
    name = name_entry.get()
    if plan == "free":
        alert("[Remotre] Please buy our premium plan to use this feature")
    if plan == "basic":
        alert("[Remotre] Please buy our premium plan to use this feature")
    if plan == "premium":
        alert(f"[Remotre] Connecting to '{name}' via FTP... Check the FTP tab.")


# Load
def load():
    global name, username, hostname, port, logins

    # Load list into variable
    logins_file = open("logins.JSON", "rb")
    logins = []
    logins = pickle.load(logins_file)
    logins_file.close()

    selected = connections_listbox.get(ACTIVE)

    # Search for the selected login in the list
    for i in logins:
        if str(selected) == str(i[0]):
            name = i[0]
            username = i[1]
            hostname = i[2]
            port = i[3]
            
            # Load
            name_entry.delete(0, END)
            name_entry.insert(0, name)

            username_entry.delete(0, END)
            username_entry.insert(0, username)

            hostname_entry.delete(0, END)
            hostname_entry.insert(0, hostname)

            port_entry.delete(0, END)
            port_entry.insert(0, port)


# Save
def save():
    global name, username, hostname, port, logins

    # Grab entries
    name = name_entry.get()
    username = username_entry.get()
    hostname = hostname_entry.get()
    port = port_entry.get()

    # Load list into variable
    logins_file = open("logins.JSON", "rb")
    logins = []
    logins = pickle.load(logins_file)
    logins_file.close()

    names = []
    for i in logins:
        names.append(i[0])
    
    # Check if login name exists
    if name in names:
        showerror(title="Error", message="This login name already exists")
    # Check if entries are empty
    elif name != "" and username != "" and hostname != "" and port != "":
        # Save to file
        logins.append([name, username, hostname, port])
        logins_file = open("logins.JSON", "wb")
        pickle.dump(logins, logins_file)
        logins_file.close()

        refresh()
    # Error if entries are empty
    else:
        showerror(title="Error",message="One or more inputs are empty")

# Refresh
def refresh():
    global name, username, hostname, port, logins

    connections_listbox.delete(0, END)

    # Load list into variable
    logins_file = open("logins.JSON", "rb")
    logins = []
    logins = pickle.load(logins_file)
    logins_file.close()

    # Load list into combobox
    for i in logins:
        connections_listbox.insert(END, i[0])


# Delete function
def delete():
    global name, username, hostname, port, logins

    selected = connections_listbox.get(ACTIVE)

    # Load list into variable
    logins_file = open("logins.JSON", "rb")
    logins = []
    logins = pickle.load(logins_file)
    logins_file.close()

    # Delete
    for i in logins:
        if str(selected) == str(i[0]):
            logins.remove(i)

    # Save to file
    logins_file = open("logins.JSON", "wb")
    pickle.dump(logins, logins_file)
    logins_file.close()

    refresh()


# RGB #
def RGB():
    global RGB_variable
    global RGB_stage
    list_RGB = list(RGB_variable)

    # Stage switching #
    # Stage 1
    if RGB_variable == (235, 52, 52):
        RGB_stage = 1
    # Stage 2
    if RGB_variable == (235, 235, 52):
        RGB_stage = 2
    # Stage 3
    if RGB_variable == (52, 235, 52):
        RGB_stage = 3
    # Stage 4
    if RGB_variable == (52, 235, 235):
        RGB_stage = 4
    # Stage 5
    if RGB_variable == (52, 52, 235):
        RGB_stage = 5
    # Stage 6
    if RGB_variable == (235, 52, 235):
        RGB_stage = 6

    # Stage 1
    if RGB_stage == 1:
        list_RGB[1] += 1
    # Stage 2
    if RGB_stage == 2:
        list_RGB[0] -= 1
    # Stage 3
    if RGB_stage == 3:
        list_RGB[2] += 1
    # Stage 4
    if RGB_stage == 4:
        list_RGB[1] -= 1
    # Stage 5
    if RGB_stage == 5:
        list_RGB[0] += 1
    # Stage 6
    if RGB_stage == 6:
        list_RGB[2] -= 1

    RGB_variable = tuple(list_RGB)
    RGB_label.configure(fg="#%02x%02x%02x" % RGB_variable)
    root.after(5, RGB)


### Window setup ###
# Window
root = Tk()
root.title("Remotre")
x_center = (root.winfo_screenwidth()/2) - (width/2)
y_center = (root.winfo_screenheight()/2) - (height/2)
root.geometry(f"{width}x{height}+{int(x_center)}+{int(y_center)}")
root.resizable(width=False, height=False)

# Images
SSH_image = PhotoImage(file = "./icons/ssh.png")
FTP_image = PhotoImage(file = "./icons/ftp.png")
load_image = PhotoImage(file = "./icons/load.png")
save_image = PhotoImage(file = "./icons/save.png")
delete_image = PhotoImage(file = "./icons/delete.png")

### Toolbar widgets ###
# Toolbar frame #
toolbar_frame = Frame(root, width=160, height=650)
toolbar_frame.grid_propagate(False)
toolbar_frame.grid(row=1, column=1)

# RGB watermark
RGB_stage = 1
RGB_variable = (235, 52, 52)
RGB_string = StringVar()
RGB_frame = Frame(toolbar_frame, width=160, height=50)
RGB_frame.grid_propagate(False)
RGB_frame.grid(row=1, column=1, sticky="nsew")
RGB_label = Label(RGB_frame, textvariable=RGB_string, fg="#%02x%02x%02x" % RGB_variable)
RGB_label["font"] = Font(size=38)
RGB_string.set("Remotre")
RGB_label.grid(row=1, column=1, sticky="nsew")
RGB()

# Connect ssh button
button(toolbar_frame, width=160, height=50, row=2, column=1, text="Connect SSH", command=connect_ssh, image=SSH_image)

# Connect ftp button
button(toolbar_frame, width=160, height=50, row=3, column=1, text="Connect FTP", command=connect_ftp, image=FTP_image)

# Connections label frame
connections_label_string = StringVar()
connections_label_frame = Frame(toolbar_frame, width=160, height=25)
connections_label_frame.grid_propagate(False)
connections_label_frame.grid(row=4, column=1)
connections_label = Label(connections_label_frame, textvariable=connections_label_string)
connections_label["font"] = Font(size=16)
connections_label_string.set("Saved Connections")
connections_label.grid(row=1, column=1)

# Connections frame #
connections_frame = Frame(toolbar_frame, width=160, height=220)
connections_frame.grid_propagate(False)
connections_frame.grid(row=5, column=1)

# Connections list frame
connections_listbox_frame = Frame(connections_frame, width=144, height=220)
connections_listbox_frame.grid_propagate(False)
connections_listbox_frame.grid(row=1, column=1)

# Listbox
connections_listbox = Listbox(connections_listbox_frame)
connections_listbox.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(connections_listbox_frame, 1, weight=1)
Grid.rowconfigure(connections_listbox_frame, 1, weight=1)

# Listbox scrollbar
connections_listbox_scrollbar = Scrollbar(connections_frame, orient="vertical")
connections_listbox_scrollbar.configure(command=connections_listbox.yview)
connections_listbox_scrollbar.grid(row=1, column=2, sticky="nsew")
connections_listbox.configure(yscrollcommand=connections_listbox_scrollbar.set)

# Entry frame #
entry_frame = Frame(toolbar_frame, width=160, height=105)
entry_frame.grid_propagate(False)
entry_frame.grid(row=6, column=1)
Grid.columnconfigure(entry_frame, 1, weight=1)

# Name
name_entry = Entry(entry_frame, bd=1)
name_entry.grid(row=1, column=1)
name_entry.insert(0, "Connection")

# Username
username_entry = Entry(entry_frame, bd=1)
username_entry.grid(row=2, column=1)
username_entry.insert(0, "root")

# Host
hostname_entry = Entry(entry_frame, bd=1)
hostname_entry.grid(row=3, column=1)
hostname_entry.insert(0, "example.com")

# Port
port_entry = Entry(entry_frame, bd=1)
port_entry.grid(row=5, column=1)
port_entry.insert(0, 22)

# Load button
button(toolbar_frame, width=160, height=50, row=7, column=1, text="Load", command=load, image=load_image)

# Save button
button(toolbar_frame, width=160, height=50, row=8, column=1, text="Save", command=save, image=save_image)

# Delete button
button(toolbar_frame, width=160, height=50, row=9, column=1, text="Delete", command=delete, image=delete_image)

### Tabs ###
# Tab frame #
tabs_frame = Frame(root, width=740, height=650)
tabs_frame.grid_propagate(False)
tabs_frame.grid(row=1, column=2)

# Tab list #
tabs = ttk.Notebook(tabs_frame)
tabs.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(tabs_frame, 1, weight=1)
Grid.rowconfigure(tabs_frame, 1, weight=1)

# Alerts tab #
alerts_frame = Frame(tabs)
tabs.add(alerts_frame, text="Alerts")

# Alerts output
alert_output = ScrolledText(alerts_frame)
alert_output.grid(row=1, column=1, sticky="nsew")
Grid.columnconfigure(alerts_frame, 1, weight=1)
Grid.rowconfigure(alerts_frame, 1, weight=1)
alert_output.configure(state="disabled")

# FTP tab #
FTP_frame = Frame(tabs)
tabs.add(FTP_frame, text="FTP")

### Account status ###
account_status_frame = Frame(root, width=900)
account_status_frame.grid(row=2, column=1, columnspan=2)
account_status_label_string = StringVar()
account_status_label = Label(account_status_frame, textvariable=account_status_label_string)
account_status_label_string.set(f"{plan.capitalize()}: {days} days remaining")
account_status_label.grid(row=1, column=1)


# Account alert
if plan == "free":
    alert(free_alert)
elif plan == "basic":
    alert(basic_alert)
elif plan == "premium":
    alert(premium_alert)

refresh()
root.mainloop()

# GUI
from tkinter import *
from tkinter import ttk
from tkinter.font import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter import filedialog

# SFTP
import pysftp as sftp

# OS detection and commands
import platform
import os

# Database
import pickle

# Others
from time import sleep
import threading
import math


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

try:
    # Load list into variable
    details_file = open("details.JSON", "rb")
    details = []
    details = pickle.load(details_file)
    details_file.close()

    # Store client details
    user = details[0]
    passwd = details[1]
    plan = details[2]
    days = details[3]

except:
    # Add client to database
    if os.path.isfile("./details.JSON") == False:
        details_file = open("details.JSON", "wb")
        details = []
        pickle.dump(details, details_file)
        details_file.close()

        user = ""
        passwd = ""
        plan = "premium"
        days = "unlimited"


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

    # Check for correct password and if plan is active
    if (password_entry.get() == "Password") and (isinstance(days, str) or days > 0):
        logged = True
        user = username_entry.get()
        passwd = password_entry.get()

        if isinstance(days, int):
            days -= 1

        # Save details
        details = [user, passwd, plan, days]
        details_file = open("details.JSON", "wb")
        pickle.dump(details, details_file)
        details_file.close()

        # Alert
        free_alert = f"[Remotre] Welcome {user}. You are currently using the free plan, upgrade to a paid plan to save connections to the cloud"
        basic_alert = f"[Remotre] Welcome {user}. You have {days} days remaining on your basic plan, upgrade to the premium plan to use the SFTP tab"
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
show_password_checkbox = Checkbutton(
    login_frame, text="Show Password", variable=show_password_checkbox_variable)
show_password_checkbox.grid(row=4, column=1, columnspan=2)

# Button
login_button_frame = Frame(login_frame, width=50, height=20)
login_button_frame.grid_propagate(False)
Grid.columnconfigure(login_button_frame, 1, weight=1)
Grid.rowconfigure(login_button_frame, 1, weight=1)
login_button_frame.grid(row=5, column=1, columnspan=2)

login_button = Button(login_button_frame, text="Login", command=login_check)
login_button.grid(row=1, column=1, sticky="nsew")

password_entry.bind("<Return>", login_check)
username_entry.bind("<Return>", login_check)

# Login error
login_error_string = StringVar()
login_error_label = Label(login_frame, fg="red",
                          textvariable=login_error_string)
login_error_label["font"] = Font(size=12)
login_error_label.grid(row=6, column=1, columnspan=2, sticky="nsew")

loop()
login_frame.mainloop()


# Show main app when login is successful
if logged == True:
    pass

else:
    exit()


### Functions ###
# Button
def button(frame, width, height, row, column, text, command, image=None):
    button_frame = Frame(frame, width=width, height=height)
    button_frame.grid_propagate(False)
    button_frame.grid(row=row, column=column)

    button = Button(button_frame, text=text, activeforeground="grey",
                    command=command, image=image, compound="left", anchor=W)
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
            os.system(
                f"osascript -e 'tell app \"Terminal\"\n do script \"ssh {username}@{hostname} -p {port}\"\n end tell'")
            alert(
                f"[SSH] Attempting to connect to '{name}' at '{username}@{hostname}:{port}' via ssh in a new terminal. Window may start minimized...")

        # Windows
        elif platform == "Windows":
            os.system(f"cmd /c start ssh {username}@{hostname} -p {port}")
            alert(
                f"[SSH] Attempting to connect to '{name}' at '{username}@{hostname}:{port}' via ssh in a new terminal...")

        else:
            alert(f"[Remotre] Sorry, your OS is not yet supported")

    except:
        alert("Entries are invalid")
    alert_output.see(END)
    alert_output.configure(state="disabled")


# Connect sftp
def connect_sftp_popup():
    def cleanup(event=None):
        global password
        password = sftp_password_entry.get()
        popup.destroy()
        SFTP_thread = threading.Thread(target=connect_sftp)
        SFTP_thread.daemon = True
        SFTP_thread.start()

    # Enter password popup window #
    popup = Toplevel()
    popup.title("Enter password for SFTP")
    x_center = (root.winfo_screenwidth()/2) - (200/2)
    y_center = (root.winfo_screenheight()/2) - (100/2)
    popup.geometry(f"{200}x{100}+{int(x_center)}+{int(y_center)}")
    popup.resizable(width=False, height=False)

    # Label
    sftp_password_label_string = StringVar()
    sftp_password_label = Label(popup, textvariable=sftp_password_label_string)
    sftp_password_label["font"] = Font(size=16)
    sftp_password_label_string.set("SFTP password:")
    sftp_password_label.grid(row=1, column=1)

    # Entry
    sftp_password_entry_frame = Frame(popup, width=200, height=26)
    sftp_password_entry_frame.grid_propagate(False)
    sftp_password_entry_frame.grid(row=2, column=1)
    Grid.rowconfigure(sftp_password_entry_frame, 2, weight=1)
    Grid.columnconfigure(sftp_password_entry_frame, 1, weight=1)

    sftp_password_entry = Entry(sftp_password_entry_frame)
    sftp_password_entry.grid(row=2, column=1)
    sftp_password_entry.configure(show="*")

    # Connect button
    connect_button_frame = Frame(popup, width=100, height=20)
    connect_button_frame.grid_propagate(False)
    Grid.columnconfigure(connect_button_frame, 1, weight=1)
    Grid.rowconfigure(connect_button_frame, 1, weight=1)
    connect_button_frame.grid(row=3, column=1, columnspan=2)

    connect_button = Button(connect_button_frame,
                            text="Connect", command=cleanup)
    connect_button.grid(row=1, column=1, sticky="nsew")

    sftp_password_entry.bind("<Return>", cleanup)

    popup.mainloop()


# Connect sftp
def connect_sftp():
    global serverpath, localpath, connection, serverpath, localpath, files, connected

    name = name_entry.get()
    username = username_entry.get()
    hostname = hostname_entry.get()
    port = port_entry.get()

    # Check if plan supports sftp
    if plan == "free":
        alert("[Remotre] Please buy our premium plan to use this feature")

    elif plan == "basic":
        alert("[Remotre] Please buy our premium plan to use this feature")

    elif plan == "premium":
        alert(
            f"[SFTP] Attemping to connect to {name} at {username}@{hostname}:{port}")

        # SFTP
        try:
            connection = sftp.Connection(
                host=hostname, username=username, password=password, port=int(port))
            serverpath = "/root"
            localpath = "/Users/sunwookim/Documents/Coding projects/SSH-Client-V2/test.txt"
            SFTP_path_string.set(serverpath)
            files = connection.listdir(serverpath)
            connection.cd(serverpath)

            # Change to SFTP tab
            tabs.select(SFTP_frame)

            # Clear listbox
            SFTP_files_listbox.delete(0, END)

            # List files
            SFTP_files_listbox.insert(END, "..")

            for f in files:
                SFTP_files_listbox.insert(END, f)

            # Claer label
            transfer_progress_string.set("")

            # SFTP connected alert
            alert(
                f"[SFTP] Connected to {name} at {username}@{hostname}:{port}")

            connected = True

        except Exception as e:
            alert(f"[SFTP] {e}")
            tabs.select(alerts_frame)


# SFTP download
def sftp_download():
    global busy

    if busy == False:
        sftp_download_thread = threading.Thread(target=sftp_download_handler)
        sftp_download_thread.daemon = True
        sftp_download_thread.start()

    else:
        showinfo(title="Please wait",
                 message="A file is being transferred. Please wait")


def sftp_download_handler():
    global busy
    selected = SFTP_files_listbox.get(ACTIVE)

    if selected != "" and connected:
        # Get local path
        localpath = filedialog.askdirectory()

        if localpath:

            # Remove '/' from the end of path
            if localpath[-1] == "/":
                localpath = localpath[:-1]

            busy = True

            # Download started popup
            showinfo(title=f"Downloading {selected}",
                     message=f"Downloading {selected}")
            # Download
            connection.get(f"{serverpath}/{selected}", f"{localpath}/{selected}",
                           callback=lambda x, y: transfer_progress(x, y))

            # Download finished popup
            showinfo(title=f"Downloaded {selected}",
                     message=f"Downloaded {selected}")

            busy = False
            transfer_progress_string.set("Done")


# Show transfer progress
def transfer_progress(x, y):
    percent = math.ceil(100.0 * x / float(y))
    filesize = f'{math.ceil(y/1024):,} KB' if y > 1024 else f'{y} bytes'
    transfer_progress_string.set(f"{percent}% of {filesize}")


# SFTP upload
def sftp_upload():
    global busy

    if busy == False:
        sftp_upload_thread = threading.Thread(target=sftp_upload_handler)
        sftp_upload_thread.daemon = True
        sftp_upload_thread.start()

    else:
        showinfo(title="Please wait",
                 message="A file is being transferred. Please wait")


def sftp_upload_handler():
    global busy

    if connected:
        localpath = filedialog.askopenfilename()
        selected = ""

        if localpath:

            # Get file name
            while localpath[-1] != "/":
                selected = localpath[-1] + selected
                localpath = localpath[:-1]

            # Remove '/' from the end of path
            if localpath[-1] == "/":
                localpath = localpath[:-1]

            busy = True

            # Uploading popup
            showinfo(title=f"Uploading {selected}",
                     message=f"Uploading {selected}")

            # Upload
            connection.put(f"{localpath}/{selected}", f"{serverpath}/{selected}",
                           callback=lambda x, y: transfer_progress(x, y))

            # Refresh files list
            sftp_refresh()

            # Upload finished popup
            showinfo(title=f"Uploaded {selected}",
                     message=f"Uploaded {selected}")

            busy = False
            transfer_progress_string.set("Done")


# SFTP refresh
def sftp_refresh():
    sftp_refresh_thread = threading.Thread(target=sftp_refresh_handler)
    sftp_refresh_thread.daemon = True
    sftp_refresh_thread.start()


def sftp_refresh_handler():
    global serverpath, localpath, connection, serverpath, localpath, files

    if connected:
        files = connection.listdir(serverpath)

        # Clear listbox
        SFTP_files_listbox.delete(0, END)

        # List files
        SFTP_files_listbox.insert(END, "..")
        for f in files:
            SFTP_files_listbox.insert(END, f)


# SFTP disconnect
def sftp_disconnect():
    global connected, busy

    if connected:
        # Disconnect
        connection.close()

        # Clear listbox
        SFTP_files_listbox.delete(0, END)

        # Clear server path
        SFTP_path_string.set("")

        connected = False
        busy = False

        # Show alert if transfer failed
        if transfer_progress_string.get() != "" and transfer_progress_string.get() != "Done":
            transfer_progress_string.set("Transfer Failed")


# SFTP actions
def sftp_action(event=None):
    global serverpath, localpath, connection, serverpath, localpath, files
    selected = SFTP_files_listbox.get(ACTIVE)

    # Prevent rapid clicking
    SFTP_files_listbox.unbind("<Double-1>")

    # Change directory
    if selected != "":

        if selected == "..":
            connection.cd(serverpath + "/..")

            while serverpath[-1] != "/":
                serverpath = serverpath[:-1]

            if serverpath[-1] == "/" and len(serverpath) > 1:
                serverpath = serverpath[:-1]
            SFTP_path_string.set(serverpath)
            sftp_refresh()

        elif connection.isdir(serverpath + "/" + selected):

            if serverpath == "/":
                serverpath = ""
            serverpath += f"/{selected}"
            SFTP_path_string.set(serverpath)
            connection.cd(serverpath)
            sftp_refresh()

        else:
            pass

    listbox_doubleclick_bind_thread = threading.Thread(
        target=listbox_doubleclick_bind)
    listbox_doubleclick_bind_thread.daemon = True
    listbox_doubleclick_bind_thread.start()


# Rebind double click
def listbox_doubleclick_bind():
    sleep(0.5)
    SFTP_files_listbox.bind("<Double-1>", sftp_action)


# SFTP menu
def sftp_menu(event):
    selected = SFTP_files_listbox.get(ACTIVE)

    if (selected != "" and selected != "..") or cp:
        # Menu contents
        menu = Menu(SFTP_files_frame, tearoff=0)
        if selected != "" and selected != "..":
            menu.add_command(
                label=f"Download '{selected}'", command=sftp_download)
            menu.add_command(
                label=f"Rename '{selected}'", command=sftp_rename_popup)
            menu.add_separator()
            menu.add_command(label=f"Copy '{selected}''", command=sftp_copy)

        if cp != "":
            menu.add_command(label=f"Paste '{cp_name}'", command=sftp_paste)

        if selected != "" and selected != "..":
            menu.add_separator()
            menu.add_command(
                label=f"Delete '{selected}'", command=sftp_delete_popup)

        # Display menu
        try:
            menu.tk_popup(event.x_root, event.y_root)

        finally:
            menu.grab_release()


# SFTP copy
def sftp_copy():
    global cp, cp_name

    selected = SFTP_files_listbox.get(ACTIVE)
    n = selected.replace(" ", "\ ")
    cp = f"{serverpath}/{n}"
    cp_name = selected.replace(" ", "\ ")


# SFTP paste
def sftp_paste():
    global cp, cp_name

    # Paste
    connection.execute(f"cp {cp} {serverpath}/{cp_name}")
    sftp_refresh()

    cp = ""
    cp_name = ""


# SFTP rename
def sftp_rename_popup():
    def cleanup(event=None):
        global newname

        newname = sftp_newname_entry.get()
        popup.destroy()
        SFTP_thread = threading.Thread(target=sftp_rename)
        SFTP_thread.daemon = True
        SFTP_thread.start()

    # Enter new name popup window #
    popup = Toplevel()
    popup.title("Enter new name for file")
    x_center = (root.winfo_screenwidth()/2) - (200/2)
    y_center = (root.winfo_screenheight()/2) - (100/2)
    popup.geometry(f"{200}x{100}+{int(x_center)}+{int(y_center)}")
    popup.resizable(width=False, height=False)

    selected = SFTP_files_listbox.get(ACTIVE)

    # Label
    sftp_newname_label_string = StringVar()
    sftp_newname_label = Label(popup, textvariable=sftp_newname_label_string)
    sftp_newname_label["font"] = Font(size=16)
    sftp_newname_label_string.set("New name:")
    sftp_newname_label.grid(row=1, column=1)

    # Entry
    sftp_newname_entry_frame = Frame(popup, width=200, height=26)
    sftp_newname_entry_frame.grid_propagate(False)
    sftp_newname_entry_frame.grid(row=2, column=1)
    Grid.rowconfigure(sftp_newname_entry_frame, 2, weight=1)
    Grid.columnconfigure(sftp_newname_entry_frame, 1, weight=1)

    sftp_newname_entry = Entry(sftp_newname_entry_frame)
    sftp_newname_entry.grid(row=2, column=1)
    sftp_newname_entry.insert(0, selected)

    # Rename button
    rename_button_frame = Frame(popup, width=100, height=20)
    rename_button_frame.grid_propagate(False)
    Grid.columnconfigure(rename_button_frame, 1, weight=1)
    Grid.rowconfigure(rename_button_frame, 1, weight=1)
    rename_button_frame.grid(row=3, column=1, columnspan=2)

    rename_button = Button(rename_button_frame, text="Rename", command=cleanup)
    rename_button.grid(row=1, column=1, sticky="nsew")

    sftp_newname_entry.bind("<Return>", cleanup)

    popup.mainloop()


def sftp_rename():
    selected = SFTP_files_listbox.get(ACTIVE)
    connection.rename(f"{serverpath}/{selected}", f"{serverpath}/{newname}")
    sftp_refresh()


# SFTP delete
def sftp_delete_popup():
    def cleanup(event=None):
        delete = sftp_delete_entry.get()
        if delete == "Confirm":
            popup.destroy()
            SFTP_thread = threading.Thread(target=sftp_delete)
            SFTP_thread.daemon = True
            SFTP_thread.start()

    # Enter new name popup window #
    popup = Toplevel()
    popup.title("Enter new name for file")
    x_center = (root.winfo_screenwidth()/2) - (200/2)
    y_center = (root.winfo_screenheight()/2) - (100/2)
    popup.geometry(f"{200}x{100}+{int(x_center)}+{int(y_center)}")
    popup.resizable(width=False, height=False)

    # Label
    sftp_delete_label_string = StringVar()
    sftp_delete_label = Label(popup, textvariable=sftp_delete_label_string)
    sftp_delete_label["font"] = Font(size=16)
    sftp_delete_label_string.set("Type 'Confirm' to delete:")
    sftp_delete_label.grid(row=1, column=1)

    # Entry
    sftp_delete_entry_frame = Frame(popup, width=200, height=26)
    sftp_delete_entry_frame.grid_propagate(False)
    sftp_delete_entry_frame.grid(row=2, column=1)
    Grid.rowconfigure(sftp_delete_entry_frame, 2, weight=1)
    Grid.columnconfigure(sftp_delete_entry_frame, 1, weight=1)

    sftp_delete_entry = Entry(sftp_delete_entry_frame)
    sftp_delete_entry.grid(row=2, column=1)

    # Confirm button
    confirm_button_frame = Frame(popup, width=100, height=20)
    confirm_button_frame.grid_propagate(False)
    Grid.columnconfigure(confirm_button_frame, 1, weight=1)
    Grid.rowconfigure(confirm_button_frame, 1, weight=1)
    confirm_button_frame.grid(row=3, column=1, columnspan=2)

    confirm_button = Button(confirm_button_frame,
                            text="Confirm", command=cleanup)
    confirm_button.grid(row=1, column=1, sticky="nsew")

    sftp_delete_entry.bind("<Return>", cleanup)

    popup.mainloop()


def sftp_delete():
    selected = SFTP_files_listbox.get(ACTIVE)
    selected = selected.replace(" ", "\ ")
    connection.execute(f"rm -rf {serverpath}/{selected}")
    sftp_refresh()


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

    # Set default port
    if isinstance(port, str):
        port = 22

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
    elif name != "" and username != "" and hostname != "":
        # Save to file
        logins.append([name, username, hostname, port])
        logins_file = open("logins.JSON", "wb")
        pickle.dump(logins, logins_file)
        logins_file.close()

        refresh()

    # Error if entries are empty
    else:
        showerror(title="Error", message="One or more inputs are empty")


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
RGB_variable = [235, 52, 52]


def RGB():
    global RGB_variable
    global RGB_stage
    list_RGB = list(RGB_variable)

    # Stage rgb values #
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

    # Stage switching #
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
    sleep(0.02)

    RGB_thread = threading.Thread(target=RGB)
    RGB_thread.daemon = True
    RGB_thread.start()


### Main App ###
# Variables
width = 1000
height = 780

cp = ""
cp_name = ""

busy = False
connected = False

name = ""
username = ""
hostname = ""
port = "22"

platform = platform.system()

serverpath = ""
localpath = ""

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

### Window setup ###
# Window
root = Tk()
root.title("Remotre")
x_center = (root.winfo_screenwidth()/2) - (width/2)
y_center = (root.winfo_screenheight()/2) - (height/2)
root.geometry(f"{width}x{height}+{int(x_center)}+{int(y_center)}")
root.minsize(width, height)

# Images
SSH_image = PhotoImage(file="./icons/ssh.png")
SFTP_image = PhotoImage(file="./icons/sftp.png")
load_image = PhotoImage(file="./icons/load.png")
save_image = PhotoImage(file="./icons/save.png")
delete_image = PhotoImage(file="./icons/delete.png")
download_image = PhotoImage(file="./icons/download.png")
upload_image = PhotoImage(file="./icons/upload.png")
refresh_image = PhotoImage(file="./icons/refresh.png")
disconnect_image = PhotoImage(file="./icons/disconnect.png")

### Toolbar widgets ###
# Toolbar frame #
toolbar_frame = Frame(root, width=160, height=755)
toolbar_frame.grid_propagate(False)
toolbar_frame.grid(row=0, column=0, sticky="nw")

# RGB watermark
RGB_stage = 1
RGB_variable = (235, 52, 52)
RGB_string = StringVar()
RGB_frame = Frame(toolbar_frame, width=160, height=50)
RGB_frame.grid_propagate(False)
Grid.columnconfigure(RGB_frame, 0, weight=1)
Grid.rowconfigure(RGB_frame, 0, weight=1)
RGB_frame.grid(row=0, column=0, sticky="nsew")
RGB_label = Label(RGB_frame, textvariable=RGB_string,
                  fg="#%02x%02x%02x" % RGB_variable)

if platform == "Darwin":
    RGB_label["font"] = Font(family="arial", size=38)

else:
    RGB_label["font"] = Font(family="arial", size=28)

RGB_string.set("Remotre")
RGB_label.grid(row=0, column=0, sticky="nsew")
RGB()

# Connect ssh button
button(toolbar_frame, width=160, height=50, row=1, column=0,
       text="Connect SSH", command=connect_ssh, image=SSH_image)

# Connect sftp button
button(toolbar_frame, width=160, height=50, row=2, column=0,
       text="Connect SFTP", command=connect_sftp_popup, image=SFTP_image)

# Connections label frame
connections_label_string = StringVar()
connections_label_frame = Frame(toolbar_frame, width=160, height=25)
connections_label_frame.grid_propagate(False)
connections_label_frame.grid(row=3, column=0)
connections_label = Label(connections_label_frame,
                          textvariable=connections_label_string)

if platform == "Darwin":
    connections_label["font"] = Font(size=16)

else:
    connections_label["font"] = Font(size=12)

connections_label_string.set("Saved Connections")
connections_label.grid(row=0, column=0, sticky="nsew")

# Connections frame #
connections_frame = Frame(toolbar_frame, width=160, height=220)
connections_frame.grid_propagate(False)
connections_frame.grid(row=4, column=0)

# Connections list frame
connections_listbox_frame = Frame(connections_frame, width=144, height=220)
connections_listbox_frame.grid_propagate(False)
connections_listbox_frame.grid(row=0, column=0)

# Listbox
connections_listbox = Listbox(connections_listbox_frame)
connections_listbox.grid(row=0, column=0, sticky="nsew")
Grid.columnconfigure(connections_listbox_frame, 0, weight=1)
Grid.rowconfigure(connections_listbox_frame, 0, weight=1)

# Listbox scrollbar
connections_listbox_scrollbar = Scrollbar(connections_frame, orient="vertical")
connections_listbox_scrollbar.configure(command=connections_listbox.yview)
connections_listbox_scrollbar.grid(row=0, column=1, sticky="nsew")
connections_listbox.configure(yscrollcommand=connections_listbox_scrollbar.set)

# Entry frame #
entry_frame = Frame(toolbar_frame, width=160, height=210)
entry_frame.grid_propagate(False)
entry_frame.grid(row=5, column=0)
Grid.columnconfigure(entry_frame, 0, weight=1)

# Name
Label(entry_frame, text="Connection Name").grid(row=0, column=0)
name_entry = Entry(entry_frame, bd=1)
name_entry.grid(row=1, column=0, sticky="nsew")

# Username
Label(entry_frame, text="Username").grid(row=2, column=0)
username_entry = Entry(entry_frame, bd=1)
username_entry.grid(row=3, column=0, sticky="nsew")

# Host
Label(entry_frame, text="Hostname").grid(row=4, column=0)
hostname_entry = Entry(entry_frame, bd=1)
hostname_entry.grid(row=5, column=0, sticky="nsew")

# Port
Label(entry_frame, text="Port").grid(row=6, column=0)
port_entry = Entry(entry_frame, bd=1)
port_entry.grid(row=7, column=0, sticky="nsew")

# Load button
button(toolbar_frame, width=160, height=50, row=6, column=0,
       text="Load", command=load, image=load_image)

# Save button
button(toolbar_frame, width=160, height=50, row=7, column=0,
       text="Save", command=save, image=save_image)

# Delete button
button(toolbar_frame, width=160, height=50, row=8, column=0,
       text="Delete", command=delete, image=delete_image)

### Tabs ###
# Tab frame #
tabs_frame = Frame(root)
tabs_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
Grid.columnconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 0, weight=1)

# Tab list #
tabs = ttk.Notebook(tabs_frame)
tabs.grid(row=0, column=0, sticky="nsew")
Grid.columnconfigure(tabs_frame, 0, weight=1)
Grid.rowconfigure(tabs_frame, 0, weight=1)

# Alerts tab #
alerts_frame = Frame(tabs)
tabs.add(alerts_frame, text="Alerts")

# Alerts output
alert_output = ScrolledText(alerts_frame)
alert_output.grid(row=0, column=0, sticky="nsew")
Grid.columnconfigure(alerts_frame, 0, weight=1)
Grid.rowconfigure(alerts_frame, 0, weight=1)
alert_output.configure(state="disabled")

# SFTP tab #
SFTP_frame = Frame(tabs)
tabs.add(SFTP_frame, text="SFTP")
Grid.columnconfigure(SFTP_frame, 0, weight=1)
Grid.rowconfigure(SFTP_frame, 1, weight=1)

# Toolbar
SFTP_toolbar_frame = Frame(SFTP_frame, height=50, borderwidth=5, relief=RIDGE)
SFTP_toolbar_frame.grid(row=0, column=0, sticky="nsew")

# Download button
button(SFTP_toolbar_frame, width=160, height=50, row=0, column=0,
       text="Download", command=sftp_download, image=download_image)

# Upload button
button(SFTP_toolbar_frame, width=160, height=50, row=0, column=1,
       text="Upload", command=sftp_upload, image=upload_image)

# Refresh button
button(SFTP_toolbar_frame, width=160, height=50, row=0, column=2,
       text="Refresh", command=sftp_refresh, image=refresh_image)

# Disconnect button
button(SFTP_toolbar_frame, width=160, height=50, row=0, column=3,
       text="Disconnect", command=sftp_disconnect, image=disconnect_image)

# Download/Upload progress
transfer_progress_string = StringVar()
transfer_progress_label = Label(
    SFTP_toolbar_frame, textvariable=transfer_progress_string)
transfer_progress_label.grid(row=0, column=4)

# SFTP explorer
SFTP_explorer_frame = Frame(SFTP_frame, borderwidth=5, relief=RIDGE)
SFTP_explorer_frame.grid(row=1, column=0, sticky="nsew")
Grid.columnconfigure(SFTP_explorer_frame, 0, weight=1)
Grid.rowconfigure(SFTP_explorer_frame, 1, weight=1)

# Path
SFTP_path_frame = Frame(SFTP_explorer_frame, height=30,
                        borderwidth=5, relief=RIDGE)
SFTP_path_frame.grid(row=0, column=0, sticky="nsew")

SFTP_path_string = StringVar()
SFTP_path_label = Label(SFTP_path_frame, textvariable=SFTP_path_string)
SFTP_path_label.grid(row=0, column=0, sticky="nsew")

# Files
SFTP_files_frame = Frame(SFTP_explorer_frame, borderwidth=5, relief=RIDGE)
SFTP_files_frame.grid(row=1, column=0, sticky="nsew")

# Listbox
SFTP_files_listbox = Listbox(SFTP_files_frame, borderwidth=0)
SFTP_files_listbox.grid(row=0, column=0, sticky="nsew")
Grid.columnconfigure(SFTP_files_frame, 0, weight=1)
Grid.rowconfigure(SFTP_files_frame, 0, weight=1)

SFTP_files_listbox.bind("<Double-1>", sftp_action)

if platform == "Darwin":
    SFTP_files_listbox.bind("<Button-2>", sftp_menu)

else:
    SFTP_files_listbox.bind("<Button-3>", sftp_menu)

# Listbox scrollbar
SFTP_files_listbox_scrollbar = Scrollbar(SFTP_files_frame, orient="vertical")
SFTP_files_listbox_scrollbar.configure(command=SFTP_files_listbox.yview)
SFTP_files_listbox_scrollbar.grid(row=0, column=1, sticky="nsew")
SFTP_files_listbox.configure(yscrollcommand=SFTP_files_listbox_scrollbar.set)

### Account status ###
account_status_frame = Frame(root, width=900)
account_status_frame.grid(row=2, column=0, columnspan=2)
account_status_label_string = StringVar()
account_status_label = Label(
    account_status_frame, textvariable=account_status_label_string)
account_status_label_string.set(f"{plan.capitalize()}: {days} days remaining")
account_status_label.grid(row=0, column=0)

# Account alert
if plan == "free":
    alert(free_alert)

elif plan == "basic":
    alert(basic_alert)

elif plan == "premium":
    alert(premium_alert)

refresh()
root.mainloop()

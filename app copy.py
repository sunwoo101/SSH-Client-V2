from tkinter import *
from tkinter import ttk
from tkinter.font import *
from tkinter.scrolledtext import *
import platform
import os
import pysftp
import mysql.connector


# Variables
width = 900
height = 670

name = ""
username = ""
hostname = ""
port = ""
password = ""
platform = platform.system()
RGB_variable = [235, 52, 52]





### Window setup ###
# Window
root = Tk()
root.title("Remotre")
x_center = (root.winfo_screenwidth()/2) - (width/2)
y_center = (root.winfo_screenheight()/2) - (height/2)
root.geometry(f"{width}x{height}+{int(x_center)}+{int(y_center)}")
root.resizable(width=False, height=False)


# Main App
class main:

    def __init__(self, master):
        ### Functions ###
        # Button
        def button(frame, width, height, row, column, text, command, image=None):
            button_frame = Frame(frame, width=width, height=height)
            button_frame.grid_propagate(False)
            button_frame.grid(row=row, column=column)

            self.button = Button(button_frame, text=text, activeforeground="grey", command=command, image=image, compound="left", anchor=W)
            self.button.grid(row=1, column=1, sticky="nsew")
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
            host = host_entry.get()
            port = port_entry.get()

            # Set default port
            if type(port) != int:
                port = 22
            if port == "":
                port = 22

            try:
                # Mac
                if platform == "Darwin":
                    os.system(f"osascript -e 'tell app \"Terminal\"\n do script \"ssh {username}@{host} -p {port}\"\n end tell'")
                    alert(f"[Remotre] Connecting to '{name}' at '{username}@{host}:{port}' via ssh in a new terminal. Window may start minimized...")
                # Windows
                elif platform == "Windows":
                    os.system(f"cmd /c start ssh {username}@{host} -p {port}")
                    alert(f"[Remotre] Connecting to '{name}' at '{username}@{host}:{port}' via ssh in a new terminal...")
                # Linux
                elif platform == "Linux":
                    os.system(f"gnome-terminal -e 'bash -c \"\"ssh {username}@{host} -p {port}\";bash\"'")
                    alert(f"[Remotre] Connecting to '{name}' at '{username}@{host}:{port}' via ssh in a new terminal...")
                else:
                    alert(f"[Remotre] Sorry, your OS is not yet supported")
            except:
                print("Entries are invalid")
            alert_output.see(END)
            alert_output.configure(state="disabled")


        # Connect ftp
        def connect_ftp():
            name = name_entry.get()
            alert(f"[Remotre] Connecting to '{name}' via FTP... Check the FTP tab.")


        # Load
        def load():
            name = name_entry.get()
            alert(f"[Remotre] Loaded '{name}'")


        # Save
        def save():
            name = name_entry.get()
            alert(f"[Remotre] Saved '{name}'")


        # Delete
        def delete():
            name = name_entry.get()
            alert(f"[Remotre] Deleted '{name}'")

            name_entry.delete(0, END)
            username_entry.delete(0, END)
            host_entry.delete(0, END)
            port_entry.delete(0, END)


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
        # Images
        self.SSH_image = PhotoImage(file = "./icons/ssh.png")
        self.FTP_image = PhotoImage(file = "./icons/ftp.png")
        self.load_image = PhotoImage(file = "./icons/load.png")
        self.save_image = PhotoImage(file = "./icons/save.png")
        self.delete_image = PhotoImage(file = "./icons/delete.png")

        ### Toolbar widgets ###
        # Toolbar frame #
        self.toolbar_frame = Frame(root, width=160, height=650)
        self.toolbar_frame.grid_propagate(False)
        self.toolbar_frame.grid(row=1, column=1)

        # RGB watermark
        RGB_stage = 1
        RGB_variable = (235, 52, 52)
        RGB_string = StringVar()
        RGB_frame = Frame(self.toolbar_frame, width=160, height=50)
        RGB_frame.grid_propagate(False)
        RGB_frame.grid(row=1, column=1, sticky="nsew")
        RGB_label = Label(self.RGB_frame, textvariable=self.RGB_string, fg="#%02x%02x%02x" % RGB_variable)
        RGB_label["font"] = Font(size=38)
        RGB_string.set("Remotre")
        RGB_label.grid(row=1, column=1, sticky="nsew")
        RGB()

        # Connect ssh button
        self.button(toolbar_frame, width=160, height=50, row=2, column=1, text="Connect SSH", command=connect_ssh, image=SSH_image)

        # Connect ftp button
        self.button(toolbar_frame, width=160, height=50, row=3, column=1, text="Connect FTP", command=connect_ftp, image=FTP_image)

        # Connections label frame
        self.connections_label_string = StringVar()
        self.connections_label_frame = Frame(toolbar_frame, width=160, height=25)
        self.connections_label_frame.grid_propagate(False)
        self.connections_label_frame.grid(row=4, column=1)
        self.connections_label = Label(connections_label_frame, textvariable=connections_label_string)
        self.connections_label["font"] = Font(size=16)
        self.connections_label_string.set("Saved Connections")
        self.connections_label.grid(row=1, column=1)

        # Connections frame #
        self.connections_frame = Frame(toolbar_frame, width=160, height=220)
        self.connections_frame.grid_propagate(False)
        self.connections_frame.grid(row=5, column=1)

        # Connections list frame
        self.connections_listbox_frame = Frame(connections_frame, width=144, height=220)
        self.connections_listbox_frame.grid_propagate(False)
        self.connections_listbox_frame.grid(row=1, column=1)

        # Listbox
        self.connections_listbox = Listbox(connections_listbox_frame)
        self.connections_listbox.grid(row=1, column=1, sticky="nsew")
        self.Grid.columnconfigure(connections_listbox_frame, 1, weight=1)
        self.Grid.rowconfigure(connections_listbox_frame, 1, weight=1)

        # Listbox scrollbar
        self.connections_listbox_scrollbar = Scrollbar(connections_frame, orient="vertical")
        self.connections_listbox_scrollbar.configure(command=connections_listbox.yview)
        self.connections_listbox_scrollbar.grid(row=1, column=2, sticky="nsew")
        self.connections_listbox.configure(yscrollcommand=connections_listbox_scrollbar.set)

        for x in range(100):
            self.connections_listbox.insert(END, f"Server {str(x+1)}")

        # Entry frame #
        self.entry_frame.grid_propagate(False)
        self.entry_frame = Frame(toolbar_frame, width=160, height=105)
        self.entry_frame.grid(row=6, column=1)
        self.Grid.columnconfigure(entry_frame, 1, weight=1)

        # Name
        self.name_entry = Entry(entry_frame, bd=1)
        self.name_entry.grid(row=1, column=1)
        self.name_entry.insert(0, "Public Pi")

        # Username
        self.username_entry = Entry(entry_frame, bd=1)
        self.username_entry.grid(row=2, column=1)
        self.username_entry.insert(0, "root")

        # Host
        self.host_entry = Entry(entry_frame, bd=1)
        self.host_entry.grid(row=3, column=1)
        self.host_entry.insert(0, "sunwooserver.ddns.net")

        # Port
        self.port_entry = Entry(entry_frame, bd=1)
        self.port_entry.grid(row=5, column=1)
        self.port_entry.insert(0, "22")

        # Load button
        self.button(toolbar_frame, width=160, height=50, row=7, column=1, text="Load", command=load, image=load_image)

        # Save button
        self.button(toolbar_frame, width=160, height=50, row=8, column=1, text="Save", command=save, image=save_image)

        # Delete button
        self.button(toolbar_frame, width=160, height=50, row=9, column=1, text="Delete", command=delete, image=delete_image)

        ### Tabs ###
        # Tab frame #
        self.tabs_frame = Frame(root, width=740, height=650)
        self.tabs_frame.grid_propagate(False)
        self.tabs_frame.grid(row=1, column=2)

        # Tab list #
        self.tabs = ttk.Notebook(tabs_frame)
        self.tabs.grid(row=1, column=1, sticky="nsew")
        self.Grid.columnconfigure(tabs_frame, 1, weight=1)
        self.Grid.rowconfigure(tabs_frame, 1, weight=1)

        # Alerts tab #
        self.alerts_frame = Frame(tabs)
        self.tabs.add(alerts_frame, text="Alerts")

        # Alerts output
        self.alert_output = ScrolledText(alerts_frame)
        self.alert_output.grid(row=1, column=1, sticky="nsew")
        self.Grid.columnconfigure(alerts_frame, 1, weight=1)
        self.Grid.rowconfigure(alerts_frame, 1, weight=1)
        self.alert_output.configure(state="disabled")

        # FTP tab #
        self.FTP_frame = Frame(tabs)
        self.tabs.add(FTP_frame, text="FTP")

        ### Account status ###
        self.account_status_frame = Frame(root, width=900)
        self.account_status_frame.grid(row=2, column=1, columnspan=2)
        self.account_status_label_string = StringVar()
        self.account_status_label = Label(account_status_frame, textvariable=account_status_label_string)
        self.account_status_label_string.set("Trial: 30 days remaining")
        self.account_status_label.grid(row=1, column=1)

app = main(root)
root.mainloop()

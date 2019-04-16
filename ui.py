from tkinter import *

class PyFocalsGUI:
    def __init__(self, master):
        self.master = master
        master.title("PyFocals")

        self.menuBar = Menu(master)

        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Open", command=None)
        self.fileMenu.add_command(label="Save", command=None)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=master.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        self.settingsMenu = Menu(self.menuBar, tearoff=0)
        self.settingsMenu.add_checkbutton(label="Verticies", command=None)
        self.settingsMenu.add_checkbutton(label="Show Camera", command=None)
        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label="Clear bindings", command=None)
        self.menuBar.add_cascade(label="Settings", menu=self.settingsMenu)

        self.optionsFrame = Frame(master, width=240, height=360, bd=2, relief=SUNKEN)
        self.optionsFrame.pack(side=RIGHT)

        self.videoFrame = Frame(master, width=360, height=360, bd=2, relief=SUNKEN)
        self.videoFrame.pack(side=LEFT)

        self.bindingListBox = Listbox(self.optionsFrame)
        self.bindingListBox.insert(1, "Left Wink")
        self.bindingListBox.insert(2, "Right Wink")
        self.bindingListBox.insert(3, "Eyebrows Up")
        self.bindingListBox.insert(4, "Open Mouth")
        self.bindingListBox.insert(5, "Head Left")
        self.bindingListBox.insert(6, "Head Right")
        self.bindingListBox.insert(7, "Head Up")
        self.bindingListBox.insert(8, "Head Down")
        self.bindingListBox.pack()

        self.rebindButton = Button(self.optionsFrame, text="Rebind", command=None)
        self.rebindButton.pack()

        self.trackButton = Button(self.optionsFrame, text="Start Tracking", command=None)
        self.trackButton.pack()

        master.config(menu=self.menuBar)

    def greet(self):
        print("Greetings!")


root = Tk()
gui = PyFocalsGUI(root)
root.mainloop()

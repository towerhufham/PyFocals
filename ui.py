from tkinter import *
from PIL import ImageTk
from PIL import Image
from imutils.video import VideoStream
from time import sleep
import imutils
import threading
import cv2

from detect_blinks import FaceTracker
import binding

class PyFocalsGUI:
    def __init__(self, master, vs):
        self.master = master
        master.title("PyFocals")

        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.panel = None

        self.lastKey = None
        self.tracker = FaceTracker()

        self.menuBar = Menu(master)

        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Open", command=None)
        self.fileMenu.add_command(label="Save", command=None)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.onClose)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        self.settingsMenu = Menu(self.menuBar, tearoff=0)
        self.settingsMenu.add_checkbutton(label="Verticies", command=None)
        self.settingsMenu.add_checkbutton(label="Show Camera", command=None)
        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label="Clear bindings", command=self.clearBindings)
        self.menuBar.add_cascade(label="Settings", menu=self.settingsMenu)

        self.optionsFrame = Frame(master, width=240, height=360, bd=2, relief=SUNKEN)
        self.optionsFrame.pack(side=RIGHT)

        self.videoFrame = Frame(master, width=360, height=360, bd=2, relief=SUNKEN)
        self.videoFrame.pack(side=LEFT)

        self.bindingListBox = Listbox(self.optionsFrame)
        self.bindingListBox.insert(0, "Left Wink")
        self.bindingListBox.insert(1, "Right Wink")
        self.bindingListBox.insert(2, "Eyebrows Up")
        self.bindingListBox.insert(3, "Open Mouth")
        self.bindingListBox.insert(4, "Head Left")
        self.bindingListBox.insert(5, "Head Right")
        self.bindingListBox.insert(6, "Head Up")
        self.bindingListBox.insert(7, "Head Down")
        self.bindingListBox.pack()

        self.rebindButton = Button(self.optionsFrame, text="Bind", command=self.startBinding)
        self.rebindButton.pack()

        self.unbindButton = Button(self.optionsFrame, text="Unbind", command=self.unbind)
        self.unbindButton.pack()

        self.trackButton = Button(self.optionsFrame, text="Start Tracking", command=None)
        self.trackButton.pack()

        self.bindingLabel = Label(self.optionsFrame, text="No key to bind")
        self.bindingLabel.pack()

        master.config(menu=self.menuBar)

        self.updateBindingTable()

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        master.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def key(self, event):
        self.lastKey = event.char
        s = "Key to bind: " + self.lastKey
        self.bindingLabel.config(text=s)

    def startBinding(self):
        #this might need a better solution
        #if we find a last key pressed
        if self.lastKey:
            #get selected items
            items = self.bindingListBox.curselection()
            for index in items:
                self.bind(index, self.lastKey)
        self.updateBindingTable()

    def bind(self, index, character):
        motion = binding.motions[index]
        binding.bind(motion, character)

    def clearBindings(self):
        #this is slightly inconsistent with the way the others work
        #BUT GOOD ENOUGH SOFTWARE IS GOOD ENOUGH RIGHT
        for i in range(8):
            motion = binding.motions[i]
            binding.unbind(motion)
        self.updateBindingTable()

    def unbind(self):
        items = self.bindingListBox.curselection()
        for index in items:
            motion = binding.motions[index]
            binding.unbind(motion)
        self.updateBindingTable()

    def updateBindingTable(self):
        for i in range(8):
            motion = binding.motions[i]
            name = binding.getBindString(motion)
            self.bindingListBox.delete(i)
            self.bindingListBox.insert(i, name)

    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=360)

                self.frame = self.tracker.track(self.frame)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(self.videoFrame, image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError:", str(e))

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        #this try/catch is in case the videostream isn't up yet
        self.stopEvent.set()
        self.vs.stop()
        self.master.quit()

def startGUI():
    root = Tk()

    #setup videostream
    vs = None
    try:
        vs = VideoStream(usePiCamera=False).start()
    except:
        vs = VideoStream(usePiCamera=True).start()

    gui = PyFocalsGUI(root, vs)
    root.bind("<Key>", gui.key)
    sleep(1.0)

    root.mainloop()

if __name__ == "__main__":
    startGUI()

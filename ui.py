from tkinter import *
from PIL import ImageTk
from PIL import Image
from imutils.video import VideoStream
from time import sleep
import imutils
import threading
import cv2

from detect_blinks import FaceTracker

class PyFocalsGUI:
    def __init__(self, master, vs):
        self.master = master
        master.title("PyFocals")

        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.panel = None

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

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        master.wm_protocol("WM_DELETE_WINDOW", self.onClose)

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
    sleep(1.0)

    root.mainloop()

if __name__ == "__main__":
    startGUI()

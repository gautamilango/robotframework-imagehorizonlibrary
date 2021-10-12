from tkinter import *
from ImageDebugger.ImageDebuggerGui import ImageDebuggerGUI

class ImageDebugger:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self


    def debug(self):
        main = Tk()    
        # SHOW THE IMAGE DEBUGGER GUI
        ImageDebuggerGUI(top=main)
        main.mainloop()

    def start_keyword(self, name, attrs):
        if attrs['kwname'].upper() == 'IMAGE DEBUGGER':    
            self.debug()



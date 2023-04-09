from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

class Main():
    def __init__(self):
        self.root = Tk()
        self.root.title("Flow")
        # self.root.iconbitmap("./assets/images/logo/logo_chico_oscuro.ico")
        self.root.minsize(width = 800, height = 500)
        
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)

        self.TFrameRed = ttk.Style()
        self.TFrameRed.configure("red.TFrame", background = "red")

        self.TFrameBlue = ttk.Style()
        self.TFrameBlue.configure("blue.TFrame", background = "blue")

        self.TFrameBlue = ttk.Style()
        self.TFrameBlue.configure("green.TFrame", background = "green")


        # self.logo_image = Image.open("./assets/images/logo/logo_oscuro.png")
        # self.logo_image = self.logo_image.resize((100, 100))
        # self.logo_image = ImageTk.PhotoImage(self.logo_image)

        SideFrame(self.root)

        self.mainFrame = ttk.Frame(
            self.root,
            style = "blue.TFrame"
        )
        self.mainFrame.grid(column = 1, row = 0, sticky = N + S + E + W)

        self.root.mainloop()


class SideFrame():
    def __init__(self, container):
        self.sideFrame = ttk.Frame(
            container,
            style = "red.TFrame",
            width = 250
        )
        self.sideFrame.grid(column = 0, row = 0, sticky = N + S + E + W)
        self.sideFrame.columnconfigure(0, weight = 1, minsize = 250)
        self.sideFrame.rowconfigure(1, weight = 1)

        
        self.titleFrame = ttk.Frame(
            self.sideFrame,
            height = 75,
            width = 250
        )
        self.titleFrame.grid(column = 0, row = 0, sticky = N + E + W)
        self.titleFrame.columnconfigure(0, minsize = 250)
        self.titleFrame.rowconfigure(0, minsize = 75)

        Label(
            self.titleFrame,
        ).grid()
        Label(
            self.titleFrame,
            text = "CHATS",
            font = "Verdana 17"
        ).grid()


        self.convFrame = ttk.Frame(
            self.sideFrame
        )
        self.convFrame.grid(sticky = S + W + E + N)
        self.convFrame.columnconfigure(0, minsize = 250)



        contactListSim = ["(1100) 12345678901234578", "que", "tal", "estas"] # Limitar a 20 caracteres el nombre de contacto

        for contact in contactListSim:
            Button(
                self.convFrame,
                text = contact,
                font = "Verdana 12",
                background = "#B948FF",
                foreground = "white"
            ).grid(sticky = W + E + N + S)

        for row in range(self.convFrame.grid_size()[1]):
            self.convFrame.rowconfigure(row, minsize = 60)
            

app = Main()
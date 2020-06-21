from tkinter import *

class Menu():

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.root = Tk()
        self.root.wm_attributes("-transparentcolor", 'grey')
        self.root.attributes('-alpha', 0.0)
        self.root.iconify()
        self.backImage = PhotoImage(file="Untitled.png")

        self.side = 1024
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.x_coord = int((screen_width / 2) - (self.side / 2))
        self.y_coord = int((screen_height / 2) - (self.side / 2))
        self.settings = 1
        self.openMenu()

    def getSets(self):
        return self.settings

    def backToMenu(self):
        self.settings = {'turn': self.turnVar.get(), 'difficulty': self.diffVar.get(), 'size': self.sizeVar.get(), 'style': self.styleVar.get().split(', ')}
        self.settingsMenuWindow.destroy()
        self.openMenu()

    def finishDefault(self):
        if self.settings == 1:
            self.settings = {'turn': True, 'difficulty': 2, 'size': 8, 'style': ['grey', 'black', 'red']}
        self.selfDestroy()

    def selfDestroy(self):
        self.game.settings = self.getSets()
        self.root.destroy()
        self.game.goOn()

    def openMenu(self):
        self.mainMenuWindow = Toplevel(self.root)
        self.mainMenuWindow.wm_attributes("-transparentcolor", 'grey')
        self.mainMenuWindow.geometry("{}x{}+{}+{}".format(self.side, self.side, self.x_coord, self.y_coord))
        self.mainMenuWindow.overrideredirect(1)

        self.backMainImage = Label(self.mainMenuWindow, image=self.backImage, bg='grey')
        self.backMainImage.pack()

        self.playB = Button(self.mainMenuWindow, text='PLAY', font=("Comic Sans MS", 20, "bold"),
                            bg='#b6f0d0', fg='#326bb8', activebackground='#9ad9d8', command=self.finishDefault)
        self.playB.pack()
        self.playB.place(bordermode=INSIDE, height=65, width=160, relx=0.40, rely=0.3)

        self.settingsB = Button(self.mainMenuWindow, text='SETTINGS', font=("Comic Sans MS", 20, "bold"),
                                bg='#b6f0d0', fg='#326bb8', activebackground='#9ad9d8', command=self.openSettings)
        self.settingsB.pack()
        self.settingsB.place(bordermode=INSIDE, height=65, width=160, relx=0.40, rely=0.4)

        self.quitB = Button(self.mainMenuWindow, text='QUIT', font=("Comic Sans MS", 20, "bold"),
                            bg='#b6f0d0', fg='#326bb8', activebackground='#9ad9d8', command=lambda: self.root.destroy())
        self.quitB.pack()
        self.quitB.place(bordermode=INSIDE, height=65, width=160, relx=0.40, rely=0.5)

        self.root.mainloop()

    def openSettings(self):
        self.mainMenuWindow.destroy()
        self.settingsMenuWindow = Toplevel(self.root)
        self.settingsMenuWindow.wm_attributes("-transparentcolor", 'grey')
        self.settingsMenuWindow.geometry("{}x{}+{}+{}".format(self.side, self.side, self.x_coord, self.y_coord))
        self.settingsMenuWindow.overrideredirect(1)

        self.backSetImage = Label(self.settingsMenuWindow, image=self.backImage, bg='grey')
        self.backSetImage.pack()

        self.setlabel = Label(self.settingsMenuWindow, bg='#b6f0d0', text="SETTINGS", font=("Comic Sans MS", 30, "bold"))
        self.setlabel.place(x=400, y=250)

        # DIFFICULTY
        self.difframe = Frame(self.settingsMenuWindow, bg='#b6f0d0', height=200, width=150)
        self.difframe.place(x=280, y=330)

        self.difflabel = Label(self.difframe, bg='#b6f0d0', text="Difficulty", font=("Comic Sans MS", 18, "bold"))
        self.difflabel.place(x=20, y=10)

        self.diffVar = IntVar()
        self.diffVar.set(2)

        self.RD1 = Radiobutton(self.difframe, variable=self.diffVar, text="Easy", value=1, font=("Comic Sans MS", 14),
                               bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RD1.place(x=17, y=60)

        self.RD2 = Radiobutton(self.difframe, variable=self.diffVar, text="Medium", value=2, font=("Comic Sans MS", 14),
                               bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RD2.place(x=17, y=100)

        self.RD3 = Radiobutton(self.difframe, variable=self.diffVar, text="Hard", value=3, font=("Comic Sans MS", 14),
                               bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RD3.place(x=17, y=140)

        # STYLE
        self.themeframe = Frame(self.settingsMenuWindow, bg='#b6f0d0', height=200, width=150)
        self.themeframe.place(x=590, y=330)

        self.themelabel = Label(self.themeframe, bg='#b6f0d0', text="Theme", font=("Comic Sans MS", 18, "bold"))
        self.themelabel.place(x=30, y=10)

        self.styleVar = StringVar()
        self.styleVar.set('grey, black, red')

        self.RT1 = Radiobutton(self.themeframe, text="Style 1", variable=self.styleVar, font=("Comic Sans MS", 14),
                               value='grey, black, red',
                               bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RT1.place(x=7, y=60)

        self.RT2 = Radiobutton(self.themeframe, text="Style 2", variable=self.styleVar, font=("Comic Sans MS", 14),
                               value='medium orchid, lavender, salmon', #'#a249a4 #c8bfe7 #de7276'
                               bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RT2.place(x=7, y=100)

        self.RT3 = Radiobutton(self.themeframe, text="Style 3", variable=self.styleVar, font=("Comic Sans MS", 14),
                               value='cornflower blue, green yellow, yellow', #''#7092be'  '#b4e61d' '#fff200''
                               bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RT3.place(x=7, y=140)

        # FIRST TURN
        self.ftFrame = Frame(self.settingsMenuWindow, bg='#b6f0d0', height=160, width=150)
        self.ftFrame.place(x=280, y=550)

        self.ftLabel = Label(self.ftFrame, bg='#b6f0d0', text="First Turn", font=("Comic Sans MS", 18, "bold"))
        self.ftLabel.place(x=14, y=10)

        self.turnVar = BooleanVar()
        self.turnVar.set(True)

        self.RFt1 = Radiobutton(self.ftFrame, text="Player", variable=self.turnVar, value=True, font=("Comic Sans MS", 14),
                                bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RFt1.place(x=7, y=60)

        self.RFt2 = Radiobutton(self.ftFrame, text="Computer", variable=self.turnVar, value=False, font=("Comic Sans MS", 14),
                                bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RFt2.place(x=7, y=100)

        # BOARD SIZE
        self.bsframe = Frame(self.settingsMenuWindow, bg='#b6f0d0', height=160, width=150)
        self.bsframe.place(x=590, y=550)

        self.bslabel = Label(self.bsframe, bg='#b6f0d0', text="Board Size", font=("Comic Sans MS", 18, "bold"))
        self.bslabel.place(x=12, y=10)

        self.sizeVar = IntVar()
        self.sizeVar.set(8)

        self.RBs1 = Radiobutton(self.bsframe, text="6x6", variable=self.sizeVar, value=6, font=("Comic Sans MS", 14),
                                bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RBs1.place(x=7, y=60)

        self.RBs2 = Radiobutton(self.bsframe, text="8x8", variable=self.sizeVar, value=8, font=("Comic Sans MS", 14),
                                bg='#b6f0d0', fg='#326bb8', activebackground='#b6f0d0')
        self.RBs2.place(x=7, y=100)

        self.backB = Button(self.settingsMenuWindow, text='Back', font=("Comic Sans MS", 20, "bold"),
                            bg='#b6f0d0', fg='#326bb8', activebackground='#9ad9d8', command=self.backToMenu)
        self.backB.place(bordermode=INSIDE, height=40, width=140, x=440, y=720)
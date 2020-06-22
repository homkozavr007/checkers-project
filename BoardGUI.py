import tkinter
from CheckerGame import *
import time

class BoardGUI():
    def __init__(self, game):
        # Initialize parameters
        self.game = game
        self.style = self.game.style
        self.ROWS = self.game.size
        self.COLS = self.game.size
        self.WINDOW_WIDTH = 720
        self.WINDOW_HEIGHT = 720
        self.col_width = self.WINDOW_WIDTH / self.COLS
        self.row_height = self.WINDOW_HEIGHT / self.ROWS
        # Initialize GUI
        self.initBoard()

    def initBoard(self):
        self.root = tkinter.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.x_coord = int((screen_width / 2) - (self.WINDOW_WIDTH / 2))
        self.y_coord = int((screen_height / 2) - (self.WINDOW_HEIGHT / 2))
        self.root.geometry("{}x{}+{}+{}".format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.x_coord, self.y_coord))
        #self.root.iconify()
        #self.window = tkinter.Toplevel(self.root)
        #self.window.geometry("100x100")  # Whatever size
        #self.window.overrideredirect(1)

        self.c = tkinter.Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT,
                                borderwidth=5, background='white')
        self.c.pack()
        self.board = [[0]*self.COLS for _ in range(self.ROWS)]
        self.tiles = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        # Print dark squares
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if (i + j) % 2 == 1:
                    self.c.create_rectangle(i * self.row_height, j * self.col_width,
                                            (i+1) * self.row_height, (j+1) * self.col_width, fill=self.style[0], outline="gray")

        # Print grid lines
        for i in range(self.ROWS):
            self.c.create_line(0, self.row_height * i, self.WINDOW_WIDTH, self.row_height * i, width=2)
            self.c.create_line(self.col_width * i, 0, self.col_width * i, self.WINDOW_HEIGHT, width=2)

        # Place checks on the board
        self.updateBoard()

        # Initialize parameters
        self.checkerSelected = False
        self.clickData = {"row": 0, "col": 0, "checker": None}

        # Register callback function for mouse clicks
        self.c.bind("<Button-1>", self.processClick)

        # make GUI updates board every second
        self.root.after(1000, self.updateBoard)


    def startGUI(self):
        self.root.mainloop()

    def pauseGUI(self):
        self.c.bind("<Button-1>", '')

    def resumeGUI(self):
        self.c.bind("<Button-1>", self.processClick)

    # Update the positions of checkers
    def updateBoard(self):
        if self.game.isBoardUpdated():
            newBoard = self.game.getBoard()
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] != newBoard[i][j]:
                        self.board[i][j] = newBoard[i][j]
                        self.c.delete(self.tiles[i][j])
                        self.tiles[i][j] = None
                        # choose different color for different player's checkers
                        if newBoard[i][j] < 0:
                            self.tiles[i][j] = self.c.create_oval(j*self.col_width+10, i*self.row_height+10,
                                                                  (j+1)*self.col_width-10, (i+1)*self.row_height-10,
                                                                  fill=self.style[2])
                        elif newBoard[i][j] > 0:
                            self.tiles[i][j] = self.c.create_oval(j*self.col_width+10, i*self.row_height+10,
                                                                  (j+1)*self.col_width-10, (i+1)*self.row_height-10,
                                                                  fill=self.style[1])
                        else:  # no checker
                            continue

                        # raise the tiles to highest layer
                        self.c.tag_raise(self.tiles[i][j])

            # tell game logic that GUI has updated the board
            self.game.completeBoardUpdate()
        # make GUI updates board every second
        self.root.after(1000, self.updateBoard)

    # this function checks if the checker belongs to the current player
    # if isPlayerTurn() returns True, then it is player's turn and only
    # postive checkers can be moved. Vice versa.
    def isCurrentPlayerChecker(self, row, col):
        return self.game.isPlayerTurn() == (self.board[row][col] > 0)

    # callback function that process user's mouse clicks
    def processClick(self, event):
        col = int(event.x // self.col_width)
        row = int(event.y // self.row_height)

        # If there is no checker being selected
        if not self.checkerSelected:
            # there exists a checker at the clicked position
            # and the checker belongs to the current player
            if self.board[row][col] != 0 and self.isCurrentPlayerChecker(row, col):
                self.clickData["row"] = row
                self.clickData["col"] = col
                self.clickData["color"] = self.c.itemcget(self.tiles[row][col], 'fill')

                # replace clicked checker with a temporary checker
                self.c.delete(self.tiles[row][col])
                self.tiles[row][col] = self.c.create_oval(col*self.col_width+10, row*self.row_height+10,
                                                         (col+1)*self.col_width-10, (row+1)*self.row_height-10,
                                                          fill=self.style[3])
                self.checkerSelected = True

            else:  # no checker at the clicked position
                return

        else: # There is a checker being selected
            # First reset the board
            oldrow = self.clickData["row"]
            oldcol = self.clickData["col"]
            self.c.delete(self.tiles[oldrow][oldcol])
            self.tiles[oldrow][oldcol] = self.c.create_oval(oldcol*self.col_width+10, oldrow*self.row_height+10,
                                                            (oldcol+1)*self.col_width-10, (oldrow+1)*self.row_height-10,
                                                            fill=self.clickData["color"])

            # If the destination leads to a legal move
            self.game.move(self.clickData["row"], self.clickData["col"], row, col)
            self.checkerSelected = False

    def destroyChecker(self, x, y, isMe):
        if isMe:
            colorTake = self.style[1]
        else:
            colorTake = self.style[2]
        for i in range(10):
            self.disappearingChecker = self.c.create_oval(x * self.col_width + (10 - i),
                                                          y * self.row_height + (10 - i),
                                                          (x + 1) * self.col_width - (10 - i),
                                                          (y + 1) * self.row_height - (10 - i),
                                                          fill=colorTake)
            time.sleep(0.05)
            self.c.delete(self.disappearingChecker)

    def win(self, score):
        time.sleep(2)
        self.c.delete(all)
        self.c.create_text(375, 355, text="Player won by {0:d} checkers!\nCongratulation!".format(score),
                           font="Verdana 30 bold", justify='center', fill='green yellow')
        self.c.create_text(370, 350, text="Player won by {0:d} checkers!\nCongratulation!".format(score),
                           font="Verdana 30 bold", justify='center')
        time.sleep(5)
        self.root.destroy()

    def lose(self, score):
        time.sleep(2)
        self.c.delete(all)
        self.c.create_text(365, 355, text="Computer won by {0:d} checkers!\nLoser!".format(score),
                           font="Verdana 30 bold", justify='center', fill='red')
        self.c.create_text(360, 350, text="Computer won by {0:d} checkers!\nLoser!".format(score),
                           font="Verdana 30 bold", justify='center')
        time.sleep(5)
        self.root.destroy()

    def draw(self):
        time.sleep(2)
        self.c.delete(all)
        self.c.create_text(375, 355, text="It is a draw!\nNot bad!",
                           font="Verdana 30 bold", justify='center', fill='yellow')
        self.c.create_text(370, 350, text="It is a draw!\nNot bad!",
                           font="Verdana 30 bold", justify='center')
        time.sleep(5)
        self.root.destroy()


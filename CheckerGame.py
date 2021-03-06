import tkinter
import time
import _thread
from AIPlayer import *
from BoardGUI import *
from Menu import *

class CheckerGame():
    def __init__(self):
        self.lock = _thread.allocate_lock()
        self.menu = Menu(self)


    def goOn(self):
        self.playerTurn = self.settings['turn']
        self.difficulty = self.settings['difficulty']
        self.size = self.settings['size']
        self.style = self.settings['style']

        if self.size == 8:
            self.board = self.initBigBoard()
        else:
            self.board = self.initSmallBoard()

        self.AIPlayer = AIPlayer(self, self.difficulty)
        self.GUI = BoardGUI(self)

        # AI goes first
        if not self.isPlayerTurn():
            _thread.start_new_thread(self.AIMakeMove, ())

        self.GUI.startGUI()

    # This function initializes the game board of small size.
    # Each checker has a label. Positive checkers for the player,
    # and negative checkers for the opponent.
    def initSmallBoard(self):
        board = [[0]*6 for _ in range(6)]
        self.kingCheckers = set()
        self.playerCheckers = set()
        self.opponentCheckers = set()
        self.checkerPositions = {}
        for i in range(6):
            self.playerCheckers.add(i + 1)
            self.opponentCheckers.add(-(i + 1))
            if i % 2 == 0:
                board[1][i] = -(i + 1)
                board[5][i] = i + 1
                self.checkerPositions[-(i + 1)] = (1, i)
                self.checkerPositions[i + 1] = (5, i)
            else:
                board[0][i] = -(i + 1)
                board[4][i] = i + 1
                self.checkerPositions[-(i + 1)] = (0, i)
                self.checkerPositions[i + 1] = (4, i)

        self.boardUpdated = True
        return board

    # This function initializes the game board of normal size.
    # Each checker has a label. Positive checkers for the player,
    # and negative checkers for the opponent.
    def initBigBoard(self):
        board = [[0] * 8 for _ in range(8)]
        self.kingCheckers = set()
        self.playerCheckers = set()
        self.opponentCheckers = set()
        self.checkerPositions = {}
        for i in range(12):
            self.playerCheckers.add(i + 1)
            self.opponentCheckers.add(-(i + 1))
            if i < 4:
                board[0][i*2+1] = -(i + 1)
                board[7][6-i*2] = i + 1
                self.checkerPositions[-(i + 1)] = (0, i*2+1)
                self.checkerPositions[i + 1] = (7, 6-i*2)
            elif i < 8:
                board[1][(i-4)*2] = -(i + 1)
                board[6][7-(i-4)*2] = i + 1
                self.checkerPositions[-(i + 1)] = (1, (i-4)*2)
                self.checkerPositions[i + 1] = (6, 7-(i-4)*2)
            else:
                board[2][i*2-15] = -(i + 1)
                board[5][22-i*2] = i + 1
                self.checkerPositions[-(i + 1)] = (2, i*2-15)
                self.checkerPositions[i + 1] = (5, 22-i*2)
        self.boardUpdated = True
        return board

    def getBoard(self):
        return self.board

    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                check = self.board[i][j]
                if check < 0:
                    print(check, end=' ')
                else:
                    print(' ' + str(check), end=' ')

            print()

    def isBoardUpdated(self):
        return self.boardUpdated

    def setBoardUpdated(self):
        self.lock.acquire()
        self.boardUpdated = True
        self.lock.release()

    def completeBoardUpdate(self):
        self.lock.acquire()
        self.boardUpdated = False
        self.lock.release()

    def isPlayerTurn(self):
        return self.playerTurn

    # Switch turns between player and opponent.
    # If one of them has no legal moves, the other can keep playing
    def changePlayerTurn(self):
        if self.playerTurn and self.opponentCanContinue():
            self.playerTurn = False
        elif not self.playerTurn and self.playerCanContinue():
            self.playerTurn = True

    # apply the given move in the game
    def move(self, oldrow, oldcol, row, col):
        if not self.isValidMove(oldrow, oldcol, row, col, self.playerTurn):
            return

        # human player can only choose from the possible actions
        if self.playerTurn and not ([oldrow, oldcol, row, col] in self.getPossiblePlayerActions()):
            return

        self.makeMove(oldrow, oldcol, row, col)
        _thread.start_new_thread(self.next, ())

    # update game state
    def next(self):
        if self.isGameOver():
            self.getGameSummary()
            return
        self.changePlayerTurn()
        if self.playerTurn:     # let player keep going
            return
        else:                   # AI's turn
            self.AIMakeMove()

    # Temporarily Pause GUI and ask AI player to make next move.
    def AIMakeMove(self):
        self.GUI.pauseGUI()
        oldrow, oldcol, row, col = self.AIPlayer.getNextMove()
        self.move(oldrow, oldcol, row, col)
        self.GUI.resumeGUI()

    # update checker position
    def makeMove(self, oldrow, oldcol, row, col):
        toMove = self.board[oldrow][oldcol]
        self.checkerPositions[toMove] = (row, col)

        # move the checker
        self.board[row][col] = self.board[oldrow][oldcol]
        self.board[oldrow][oldcol] = 0

        if row == 0 or row == self.size-1:
            self.kingCheckers.add(toMove)
        # capture move, remove captured checker
        if abs(oldrow - row) == 2:
            toRemove = self.board[(oldrow + row) // 2][(oldcol + col) // 2]
            if toRemove > 0:
                self.playerCheckers.remove(toRemove)
                self.GUI.destroyChecker((oldcol + col) // 2, (oldrow + row) // 2, True)
            else:
                self.opponentCheckers.remove(toRemove)
                self.GUI.destroyChecker((oldcol + col) // 2, (oldrow + row) // 2, False)
            self.board[(oldrow + row) // 2][(oldcol + col) // 2] = 0
            self.checkerPositions.pop(toRemove, None)

        self.setBoardUpdated()

    # Get all possible moves for the current player
    def getPossiblePlayerActions(self):
        checkers = self.playerCheckers
        regularDirs = [[-1, -1], [-1, 1]]
        captureDirs = [[-2, -2], [-2, 2]]
        kingAddRegularDirs = [[1, -1], [1, 1]]
        kingAddCaptureDirs = [[2, -2], [2, 2]]

        regularMoves = []
        captureMoves = []
        for checker in checkers:
            oldrow = self.checkerPositions[checker][0]
            oldcol = self.checkerPositions[checker][1]

            if checker in self.kingCheckers:
                for dir in kingAddRegularDirs:
                    if self.isValidMove(oldrow, oldcol, oldrow + dir[0], oldcol + dir[1], True):
                        regularMoves.append([oldrow, oldcol, oldrow + dir[0], oldcol + dir[1]])
                for dir in kingAddCaptureDirs:
                    if self.isValidMove(oldrow, oldcol, oldrow + dir[0], oldcol + dir[1], True):
                        captureMoves.append([oldrow, oldcol, oldrow + dir[0], oldcol + dir[1]])

            for dir in regularDirs:
                if self.isValidMove(oldrow, oldcol, oldrow+dir[0], oldcol+dir[1], True):
                    regularMoves.append([oldrow, oldcol, oldrow+dir[0], oldcol+dir[1]])
            for dir in captureDirs:
                if self.isValidMove(oldrow, oldcol, oldrow+dir[0], oldcol+dir[1], True):
                    captureMoves.append([oldrow, oldcol, oldrow+dir[0], oldcol+dir[1]])

        # must take capture move if possible
        if captureMoves:
            return captureMoves
        else:
            return regularMoves

    # check if the given move if valid for the current player
    def isValidMove(self, oldrow, oldcol, row, col, playerTurn):
        # invalid index
        if oldrow < 0 or oldrow > self.size-1 or oldcol < 0 or oldcol > self.size-1 \
                or row < 0 or row > self.size-1 or col < 0 or col > self.size-1:
            return False
        # No checker exists in original position
        if self.board[oldrow][oldcol] == 0:
            return False
        # Another checker exists in destination position
        if self.board[row][col] != 0:
            return False

        # player's turn

        if playerTurn:

            if self.board[oldrow][oldcol] in self.kingCheckers:
                if abs(row - oldrow) == 1:  # regular move
                    return abs(col - oldcol) == 1
                elif row - oldrow == -2:  # capture move
                    #  \ direction or / direction
                    return (col - oldcol == -2 and self.board[row + 1][col + 1] < 0) \
                           or (col - oldcol == 2 and self.board[row + 1][col - 1] < 0)
                elif row - oldrow == 2:  # capture move
                    # / direction or \ direction
                    return (col - oldcol == -2 and self.board[row - 1][col + 1] < 0) \
                           or (col - oldcol == 2 and self.board[row - 1][col - 1] < 0)
                else:
                    return False

            if row - oldrow == -1:   # regular move
                return abs(col - oldcol) == 1
            elif row - oldrow == -2:  # capture move
                #  \ direction or / direction
                return (col - oldcol == -2 and self.board[row+1][col+1] < 0) \
                       or (col - oldcol == 2 and self.board[row+1][col-1] < 0)
            else:
                return False
        # opponent's turn
        else:

            if self.board[oldrow][oldcol] in self.kingCheckers:
                if abs(row - oldrow) == 1:  # regular move
                    return abs(col - oldcol) == 1
                elif row - oldrow == -2:  # capture move
                    #  \ direction or / direction
                    return (col - oldcol == -2 and self.board[row + 1][col + 1] < 0) \
                           or (col - oldcol == 2 and self.board[row + 1][col - 1] < 0)
                elif row - oldrow == 2:  # capture move
                    # / direction or \ direction
                    return (col - oldcol == -2 and self.board[row - 1][col + 1] < 0) \
                           or (col - oldcol == 2 and self.board[row - 1][col - 1] < 0)
                else:
                    return False

            if row - oldrow == 1:   # regular move
                return abs(col - oldcol) == 1
            elif row - oldrow == 2: # capture move
                # / direction or \ direction
                return (col - oldcol == -2 and self.board[row-1][col+1] > 0) \
                       or (col - oldcol == 2 and self.board[row-1][col-1] > 0)
            else:
                return False

    # Check if the player can continue
    def playerCanContinue(self):
        directions = [[-1, -1], [-1, 1], [-2, -2], [-2, 2]]
        kingDirections = [[1, -1], [1, 1], [2, -2], [2, 2]]
        for checker in self.playerCheckers:
            position = self.checkerPositions[checker]
            row = position[0]
            col = position[1]
            for dir in directions:
                if self.isValidMove(row, col, row + dir[0], col + dir[1], True):
                    return True
            if checker in self.kingCheckers:
                for dir in kingDirections:
                    if self.isValidMove(row, col, row + dir[0], col + dir[1], True):
                        return True
        return False

    # Check if the opponent can continue
    def opponentCanContinue(self):
        directions = [[1, -1], [1, 1], [2, -2], [2, 2]]
        kingDirections = [[-1, -1], [-1, 1], [-2, -2], [-2, 2]]
        for checker in self.opponentCheckers:
            position = self.checkerPositions[checker]
            row = position[0]
            col = position[1]
            for dir in directions:
                if self.isValidMove(row, col, row + dir[0], col + dir[1], False):
                    return True
            if checker in self.kingCheckers:
                for dir in kingDirections:
                    if self.isValidMove(row, col, row + dir[0], col + dir[1], False):
                        return True
        return False

    # Neither player can can continue, thus game over
    def isGameOver(self):
        if len(self.playerCheckers) == 0 or len(self.opponentCheckers) == 0:
            return True
        else:
            return (not self.playerCanContinue()) and (not self.opponentCanContinue())

    def getGameSummary(self):
        self.GUI.pauseGUI()
        print("Game Over!")
        playerNum = len(self.playerCheckers)
        opponentNum = len(self.opponentCheckers)
        if (playerNum > opponentNum):
            print("Player won by {0:d} checkers! Congratulation!".format(playerNum - opponentNum))
            self.GUI.win(playerNum - opponentNum)
        elif (playerNum < opponentNum):
            print("Computer won by {0:d} checkers! Try again!".format(opponentNum - playerNum))
            self.GUI.lose(opponentNum - playerNum)
        else:
            print("It is a draw! Try again!")
            self.GUI.draw(playerNum - opponentNum)


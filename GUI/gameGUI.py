#GUI.py
#Game
#Abraham Oliver and Jadan Ercoli


import pygame
import Permaximize.GUI.baseGUI as parent


class GUI(parent.GUI):
    def __init__(self, game, width = 740, height = 740, circle = 37):
        self.game = game
        self.circle = circle
        super(GUI, self).__init__(width = width, height = height)

    def update(self, board, ended = False, player = False):
        #Draw all elements
        self.display.fill(self.white)
        self.drawBoard(board)
        self.displayScore()
        self.displayTurn()
        #Update all drawings
        pygame.display.update()
        #Check events
        return self.checkEvents(board, ended, player)

    def checkEvents(self, board, ended = False, player = False):
        for event in pygame.event.get():
            # Checks if window is closed
            if event.type == pygame.QUIT:
                self.close()
            # Player play events
            if player:
                # Check if mouse button is pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If so, select piece
                    self._selectPieceEvent(board)
                key = pygame.key.get_pressed()
                if key[pygame.K_RETURN]:
                    success = False
                    success = self.game.playSelected()
                    if success:
                        return True
            return False

    def _selectPieceEvent(self, board):
        loc = pygame.mouse.get_pos()
        pieceLoc = self.findRect(loc[0], loc[1])
        if pieceLoc == None:
            return
        #Checks if piece is already selected/immovable
        if not board[pieceLoc].selected and not board[pieceLoc].state:
            #Checks to see if two pieces are already selected
            if len(self.game.selected) >= 2:
                #Deselect already selected
                self.game.deselect()
                return
            #Otherwise select piece
            self.game.selected.append(pieceLoc)
            board[pieceLoc].selected = True
        else:
            board[pieceLoc].selected = False

    def drawBoard(self, board):
        #Defines variables of the rectangle
        rectWH = self.width - 100
        rectPoint = (self.width / 2) - (rectWH / 2)

        #Colors the rectangle
        #pygame.draw.rect(self.display, self.gray, [rectPoint,rectPoint,rectWH,rectWH])

        #Draw rectangle always centered on the screen
        #pygame.draw.rect(self.display, self.black, [rectPoint,rectPoint,rectWH,rectWH],4)

        """
        #Draw all seperation lines
        orig = (rectPoint, rectPoint)
        distance = rectWH / 8
        #Draws lines at increment 'distance'
        for i in range(7):
            #Draw horizontal lines
            new = (orig[0], (orig[1] + ((i + 1) * distance)))
            new2 = (orig[0] + rectWH, new[1])
            pygame.draw.line(self.display, self.black, new, new2, 2)

            #Draw vertical lines
            new3 = ((orig[0] + ((i + 1) * distance), orig[1]))
            new4 = (new3[0], orig[1] + rectWH)
            pygame.draw.line(self.display, self.black, new3, new4, 2)
        """
        #Draw all pieces
        for i in range(len(board)):
            self.drawPiece(i, board[i].color, board)

    def drawPiece(self, loc, color, board):
        rectWH = self.width - 100
        #Starting point
        rectPoint = (self.width // 2) - (rectWH // 2)
        #Distances between each half a space
        distance = (self.width - 100) // 16
        #Starting at 1 and skipping every 2
        dSet = range(1, 16, 2)
        #Find x and y coordinates on the board that is 8x8
        x = loc % 8
        y = loc // 8
        #Find center coordinates of the piece
        xpos = rectPoint + (dSet[x] * distance)
        ypos = rectPoint + (dSet[y] * distance)
        #Draw piece

        if color == 1:
            color = self.blue
        elif color == 2:
            color = self.red
        #Changes design of pieces that are permatized
        if not board[loc].state:
            pygame.draw.circle(self.display, color, [xpos,ypos], self.circle)
        if board[loc].state:
            pygame.draw.circle(self.display, color, [xpos,ypos], self.circle, 12)
        #Changes design for pieces that are currently selected
        elif board[loc].selected:
            pygame.draw.circle(self.display, self.black, [xpos,ypos], self.circle + 13, 10)

    def displayScore(self):
        #Set text to display
        score = self.game.checkScore()
        toPrint = "%s - %s" % (score[0], score[1])
        toPrintp1 = str(score[0])
        self.displayText(toPrintp1, (self.display.get_rect().centerx * .5 + 20, 27), self.blue)
        toPrintp2 = str(score[1])
        self.displayText(toPrintp2, (self.display.get_rect().centerx * .5 + 100, 27), self.red)
        # toPrintwscore = "Score:"
        # self.displayText(toPrintwscore, (self.display.get_rect().centerx * .5 -100, 25))
        toPrinth = "-"
        self.displayText(toPrinth, (self.display.get_rect().centerx * .5+ + 60, 27))

    def displayTurn(self):
            if self.game.turns % 2 == 0:
                    color = self.blue
            else:
                    color = self.red
            if self.game.turns == 20:
                    turn = "GAME OVER"
                    color = self.winColor
            else:
                    turn = "Turn # - %s" % (self.game.turns + 1)
            self.displayText(turn,(self.display.get_rect().centerx * 1.5, 25), color)
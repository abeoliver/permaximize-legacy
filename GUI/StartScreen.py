#StartScreen.py
#Game
#Abraham Oliver and Jadan Ercoli

import baseGUI as G
import pygame

class StartScreen(G.GUI):
    def update(self):
        self.fill(self.white)
        self.checkEvents()
        logo = pygame.image.load("straw.png").convert_alpha()

        # Drawing
        self.display.blit(self.background, (0,0))
        self.drawButton("Play Game", (75, 300, 600, 200), self.blue)
        self.display.blit(get_image("straw.png"),(200,200))
        

        pygame.display.flip()

g = StartScreen()

while True:
    g.update()

	

import pygame
from sys import exit

class GUI(object):
	def __init__(self, width = 740, height = 740):
		pygame.init()
		#Color declarations
		self.white = (255,255,255)
		self.black = (0,0,0)
		self.red = pygame.Color("#F44336")
		self.gray = pygame.Color("#E0E0E0")
		self.blue = pygame.Color("#2196F3")

		#Font delcarations
		self.font = pygame.font.SysFont(None, 75)

		#Screen declarations
		self.width = width
		self.height = height

		#Screen initialization
		self.display = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Game")
		self.background = pygame.Surface(self.display.get_size())

	def update(self):
		self.checkEvents()

	def findRect(self, x, y):
		#Set rect width and height
		rectWH = self.width - 100
		#Starting point
		rectPoint = (self.width / 2) - (rectWH / 2)
		#Is mouse position even valid
		if x < rectPoint or x > (rectPoint + rectWH):
			return None
		elif y < rectPoint or y > (rectPoint + rectWH):
			return None

		#Distances between each half a space
		dist = (rectWH) / 8
		#Find x and y boundries on the board that is 8x8
		for i in range(8):
			for j in range(8):
				if x >= (rectPoint + (i * dist)) and x <= (rectPoint + ((i + 1) * dist)):
					if y >= (rectPoint + (j * dist)) and y <= (rectPoint + ((j + 1) * dist)):
						#Find board location base of cartesian location
						loc = i + (j * 8)
		return loc

	def checkEvents(self):
		for event in pygame.event.get():
			# Checks if window is closed
			if event.type == pygame.QUIT:
				self.close()

	def fill(self, color):
		 self.background.fill(color)

	def displayText(self, text, loc, color = 0):
		if color == 0:
			color = self.black
		t = self.font.render(text, False, color)
		textRect = t.get_rect()
		textRect.centerx = loc[0]
		textRect.centery = loc[1]
		#Draw the text onto the surface
		self.display.blit(t, textRect)

	def drawButton (self, text, rect, color):
                pygame.draw.rect(self.display, color, rect)
                self.displayText(text, [rect[0] + rect[2]/2, rect[1] + rect[3]/2], self.white)

	def close(self):
		pygame.quit()
		exit()

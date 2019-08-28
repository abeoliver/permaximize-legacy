#PlexQueue.py
#Abraham Oliver, Plexivate Software

class Queue (object):
	def __init__(self):
		self.items = []
	
	def __len__(self):
		return len(self.items)
	
	def __getitem__(self, i):
		"""Returns item from FRONT not rear"""
		index = len(self.items) - 1 - i
		if index >= 0:
			return self.items[index]
	
	def __iter__(self):
		"""Allows for use of looping and iterations
		NOTE: Iterates from FRONT to REAR"""
		for item in self.items:
			yield item
	
	def save(self):
		"""Save current list to 'self.saved'"""
		self.saved = self.items
	
	def load(self, mode = 1):
		"""Load 'self.saved' to the current queue"""
		self.items = self.saved

	def enqueue(self, item):
		"""Adds item to rear of queue"""
		self.items.insert(0, item)
	
	def dequeue(self):
		"""Takes item from front of que"""
		return self.items.pop()
		
	def reverse(self):
		self.items.reverse()
	
	def rotate(self):
		"""Moves every item 1 space towards the front and the front item to the back"""
		if not self.isEmpty():
			top = self.dequeue()
			self.enqueue(top)
		else:
			print "Queue empty"
	
	def isEmpty(self):
		if self.items == []:
			return True
		else:
			return False

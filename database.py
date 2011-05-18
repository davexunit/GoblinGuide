import sqlite3

class Game:
	'''Encapsulates an entry in the game table.
	'''
	def __init__(self):
		self.title = 'Untitled'
		self.platform = 'NONE'
	
	def __init__(self, title, platform):
		self.title = title
		self.platform = platform

class FAQ:
	'''Encapsulates an entry in the faq table.
	'''
	def __init__(self):
		self.title = 'Untitled FAQ'
		self.author = 'Anonymous'
		self.date = '1/1/2001'
		self.version = '1.0'
	
	def __init__(self, title, author, date, version):
		self.title = title
		self.author = author
		self.date = date
		self.version = version



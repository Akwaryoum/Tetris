#!/usr/bin/python3
# Fait par Vincent Ploquien

"""Le backend gère toute la partie logique du jeu
(gestion du plateau, test de placement, ...)"""

# Dépendances
import random

# - Dépendances DEV
import pprint
pp = pprint.PrettyPrinter(indent=4)
# -

class PlacementException(Exception):
	pass

class Board:
	"""Le tableau de jeu d'une partie de Tetris
	avec sa bibliothèque de formes possibles"""
	def __init__(self, width, height, base=0):
		"""Initialise le tableau de jeu

		Keyword arguments:
		width -- la largeur du plateau
		height -- la hauteur du plateau
		base -- la valeur par défaut d'une case (défaut: 0)
		"""
		self.width = width
		self.height = height

		# Créer une matrice de taille width*height
		self.matrix = [[base for i in range(width)] for j in range(height)]

		# Créer une bibliothèques des formes possibles
		self.shapes = []

	# Gestion du plateau

	def fillMatrix(self, fillValue):
		"""Rempli le tableau de jeu avec la valeur fillValue"""
		for y in range(len(self.matrix)):
			for x in range(len(self.matrix[y])):
				self.matrix[y][x] = fillValue
	
	def clearMatrix(self):
		"""Rempli le tableau de jeu de 0"""
		self.fillMatrix(0)

	def isFree(self, x, y):
		"""Renvoie True si la case en x,y est vide"""
		return self.matrix[y][x] == 0

	def placePiece(self, piece, x, y, color=1):
		"""Insere la piece dans le tableau de jeu apres verification"""
		shape = piece.shape
		# Vérification de validité
		for i, line in enumerate(shape):
			for j, pixel in enumerate(line):
				# Vérification de l'emplacement
				try:
					isFree = self.isFree(x + i, y + j)
				except IndexError:
					raise PlacementException("La pièce dépasse du tableau de jeu")

				if not self.isFree(x + i, y + j):
					raise PlacementException("Une pièce est déjà présente")
		
		# Placement de la pièce
		for i, line in enumerate(shape):
			for j, pixel in enumerate(line):
					self.matrix[y + j][x + i] = color

	# Bibliothèques de pièces

	def addPiece(self, newPiece):
		"""Ajoute la piece newPiece dans la bibliothèques des pièces possibles"""

		# Tests de validité
		if not isinstance(newPiece, Piece):
			raise ValueError("Le paramètre newPiece n'est pas un objet Piece")

		newShape = newPiece.shape
		if len(newShape) > self.height:
			raise ValueError("La hauteur d'une pièce ne peut pas être plus grande que celle du jeu")
		previousLength = -1
		for line in newShape:
			if len(line) > self.width:
				raise ValueError("La largeur d'une pièce ne peut pas être plus grande que celle du jeu")
			if len(line) != previousLength and previousLength != -1:
				raise ValueError("La largeur de la pièce n'est pas uniforme")
			previousLength = len(line)
			if not isinstance(line[0], int):
				raise ValueError("La pièce n'est pas constituée d'entiers")

		self.shapes.append(newPiece)

	def getRandomPiece(self):
		"""Renvoie une piece valide au hasard"""
		return random.choice(self.shapes)

	def getPieceAtIndex(self, index):
		"""Renvoie une piece a l'index index"""
		return self.shapes[index]


class Piece:
	"""Une pièce de jeu, avec sa forme à elle"""
	def __init__(self, shape):
		"""Initialise la pièce

		Keyword arguments:
		shape -- tableau 2D décrivant la forme de la pièce
		"""
		self.shape = shape


# Execution du programme directement (pour le test)
if __name__ == "__main__":
	board = Board(10, 10)
	board.matrix[0][0] = 1
	pp.pprint(board.matrix)
	
	# Définitions des pièces
	carre = Piece([
			[1, 1],
			[1, 1]
	])
	colonne = Piece([
			[1],
			[1]
	])
	ligne = Piece([
			[1, 1]
	])
	board.addPiece(carre)
	board.addPiece(colonne)
	board.addPiece(ligne)
	
	try:
		board.placePiece(carre, 0, 1)
	except PlacementException:
		raise
	pp.pprint(board.matrix)

	piece = board.getRandomPiece()
	pp.pprint(piece.shape)

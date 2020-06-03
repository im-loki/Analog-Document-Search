# Dictonary Module.
# Input: Sentence or word.
# Output: Corrected Sentence or word.

from autocorrect import Speller

class my_auto_correct:

	spell = None

	def __init__(self):
		self.spell = Speller(lang='en')

	def correct(self, Sentence):
		return self.spell(Sentence)
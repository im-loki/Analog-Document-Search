from spellchecker import SpellChecker

def spell_check_me(sentence):
	spell = SpellChecker()
	spell.word_frequency.load_words(['microsoft', 'apple', 'google','hadoop','json','samsung', 'backend', 'ocr', 'keyphrase'])
	temp = ""

	for word in sentence.split(" "):
		temp += " " + spell.correction(word)

	print("SpellChecker: ", temp)
	return temp


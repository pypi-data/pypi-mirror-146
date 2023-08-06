__all__ = ['filter', 'Censor', 'Remove']


import json
import random


class Censor:
	def __init__(self, style: str | list[str] | None = '*') -> None:
		"""Replaces the word characters with the prefered style.

		Parameters:
		-----------
			'style' <str | list[str]> *(optional)* - A character or a list of characters to replace the word with.
		"""

		self.style = style

	async def generate(self, word: str) -> str:
		"""Generates the censorship to replace the word with.

		Parameters:
		-----------
			'word' <str> - The word to be replaced.

		Returns:
		--------
			str - If the style is a single characters it'll return the length of the word with that characters. If the style is a list of characters it'll return a string of 4 randomly choosen characters from the list.
		"""

		return str(self.style * len(word)) if (type(self.style) is str) else ''.join(random.choices(self.style, k=4))

class Remove:
	def __init__(self) -> None:
		"""Removes the word from the text."""
		pass


def get_banned_words(strickness: int) -> list[str]:
	"""Fetches the words to filter out from the data.json file.

	Parameters:
	-----------
		'strickness' <int> - The type of words to fetch.

	Returns:
	--------
		list[str] - A list of all the words to be detected.
	"""

	with open('data.json', 'r') as f:
		data = json.loads(f.read())

	banned_words = []
	for _strickness, data in data.items():
		if int(_strickness) <= int(strickness):
			for language, words in data.items():
				banned_words.extend(words)

	return banned_words


def detect_symbols(word: str, banned_words: list[str]) -> bool:
	"""Checks if the word has symbols that when decrypted enteruperates the word as one of those banned.

	Parameters:
	-----------
		'word' <str> - The world to be checked.
		'banned_words' <list[str]> - The list of words to match the word to.

	Returns:
	--------
		True - The symbols corrospond to letters that match the 'word' for words in 'banned_words'.
		False - The symbols doesn't affect the word meaning.
	"""

	symbols = ['*', '&', '#', '$', '.', '_', '-']
	alphabet = "abcdefghijklmnopqrstuvwxyz"

	for letter in word:
		new_word = word

		if letter in symbols:
			for character in alphabet:
				new_word.replace(letter, character)
				
				if new_word.lower() in banned_words:
					return True

	return False

def detect_spaces(word: str) -> bool:
	"""Detects spaced-out words.

	Parameters:
	-----------
		'word' <str> - The word to check.

	Returns:
	--------
		True - The word is spaced-out.
		False - The word is not spaced-out or is a 1-2 letter word.
	"""

	allowed_words = [
		'a', 
		'i', 
		'of', 
		'to',
		'in', 
		'it', 
		'is', 
		'be', 
		'as', 
		'at', 
		'so', 
		'we', 
		'he', 
		'by', 
		'or', 
		'or', 
		'on', 
		'do', 
		'if', 
		'me'
	]

	return ((len(word) < 3) and (word not in allowed_words))


def decrypt_numerology(word: str) -> str:
	"""Checks if the word is using nermology and decrypts it for it to be detected.

	Parameters:
	-----------
		'word' <str> - The world to be checked.

	Returns:
	--------
		str - The decrypted word.
	"""
	if len(word) < 2:
		return word

	numbered_characters = {
		'a': '1',
		'b': '2',
		'c': '3',
		'd': '4',
		'e': '5',
		'f': '8',
		'g': '3',
		'h': '5',
		'i': '1',
		'j': '1',
		'k': '2',
		'l': '3',
		'm': '4',
		'n': '5',
		'o': '7',
		'p': '8',
		'q': '1',
		'r': '2',
		's': '3',
		't': '4',
		'u': '6',
		'v': '6',
		'w': '6',
		'x': '5',
		'y': '1',
		'z': '7'
	 }

	for character, number in numbered_characters.items():
		for letter in word:
			if letter == number:
				word.replace(letter, character)

	return word

def decrypt_spaces(text_list: list[str], word: str) -> str:
	"""Decrypts spaced-out words.

	Parameters:
	-----------
		'text_list' <str> - The list of words for the sentence being filtered.
		'word' <str> - The current word being checked.

	Returns:
	--------
		str - The decrypted word.
	"""

	if not detect_spaces(word): return word

	for i, _word in enumerate(text_list):
		if (i > text_list.index(word)) and (detect_spaces(word)):
			word += _word

	return decrypt_numerology(word)


async def filter(text: str, strickness: int|None = 2, action: Censor|Remove = Censor()) -> None:
	"""Filters the text based on the action given with the preferred strickness level.

	Parameters:
	-----------
		'text' <str> - The text to be filtered.
		'strickness' <int> *(optional)* - The type of words to be filtered.
		'action' <Censor|Remove> *(optional)* - How to deal with the words to be filtered.

	Returns:
	--------
		str - The filtered text.
	"""
	
	banned_words = get_banned_words(strickness)
	text_list = text.split(' ')

	for i, word in enumerate(text_list):
		if (
			(word.lower() in banned_words) or # word
			(decrypt_numerology(word.lower()) in banned_words) or # w0rd
			(detect_symbols(word.lower(), banned_words)) or # w*rd
			(decrypt_spaces(text_list, word.lower()) in banned_words) # 'w o r d' OR 'w 0 r d' OR 'wo rd' OR 'w0 rd'
		):
			if type(action) is Censor:
				text_list[i] = await action.generate(word.lower())

			if type(action) is Remove:
				text_list.pop(i)

	return ' '.join(text_list)
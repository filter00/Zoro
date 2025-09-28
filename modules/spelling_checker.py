import re
from spellchecker import SpellChecker

class SpellingChecker:
    def __init__(self, language='en'):
        # pyspellchecker默認 english; agar tumko Hindi support chahiye to alag approach lagani padegi
        self.spell = SpellChecker(language=language)

    def check_spelling(self, text: str):
        words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
        misspelled = self.spell.unknown(words)
        return list(misspelled)

    def correct_word(self, word: str):
        return self.spell.correction(word)

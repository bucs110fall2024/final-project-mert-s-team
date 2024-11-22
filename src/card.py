class Card:
    def __init__(self, english_word, turkish_word):
        self.english_word = english_word
        self.turkish_word = turkish_word

    def check_answer(self, selected_word):
        return selected_word == self.turkish_word

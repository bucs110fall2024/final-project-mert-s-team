import random
from src.card import Card

class GameBoard:
    def __init__(self):
        self.score = 0
        self.flashcards = []
        self.current_card = None

    def load_flashcards(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                english, turkish = line.strip().split(',')
                self.flashcards.append(Card(english, turkish))
        self.next_card()

    def get_current_card(self):
        return self.current_card

    def next_card(self):
        if self.flashcards:
            self.current_card = random.choice(self.flashcards)

    def get_options(self):
        options = [self.current_card.turkish_word]
        while len(options) < 4:
            random_card = random.choice(self.flashcards)
            if random_card.turkish_word not in options:
                options.append(random_card.turkish_word)
        random.shuffle(options)
        return options

    def update_score(self, correct):
        if correct:
            self.score += 1

import random
from src.card import Card


class GameBoard:
    """
    Manages the collection of flashcards, game state, and scoring.
    """

    def __init__(self):
        """
        Initializes the GameBoard object.
        """
        self.score = 0
        self.flashcards = []
        self.current_card = None

    def load_flashcards(self, filepath):
        """
        Loads flashcards from a file and populates the flashcards list.

        Args:
            filepath (str): Path to the file containing flashcards in "English,Turkish" format.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file contains invalid data.
        """
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    try:
                        english, turkish = line.strip().split(',')
                        self.flashcards.append(Card(english.strip(), turkish.strip()))
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
            if not self.flashcards:
                raise ValueError("No valid flashcards found in the file.")
            self.next_card()
        except FileNotFoundError:
            raise FileNotFoundError(f"Flashcards file '{filepath}' not found.")
        except Exception as e:
            print(f"An error occurred while loading flashcards: {e}")

    def get_current_card(self):
        """
        Returns the current flashcard being displayed.

        Returns:
            Card: The current flashcard.
        """
        return self.current_card

    def next_card(self):
        """
        Advances to the next flashcard. If no flashcards remain, sets current_card to None.
        """
        if self.flashcards:
            self.current_card = random.choice(self.flashcards)
        else:
            self.current_card = None

    def get_options(self):
        """
        Generates a list of 4 answer options, including the correct answer.

        Returns:
            list: A shuffled list of 4 Turkish words (1 correct and 3 random incorrect).
        """
        if not self.current_card:
            return []

        options = [self.current_card.turkish_word]
        while len(options) < 4:
            random_card = random.choice(self.flashcards)
            if random_card.turkish_word not in options:
                options.append(random_card.turkish_word)
        random.shuffle(options)
        return options

    def check_answer(self, selected_answer):
        """
        Checks if the selected answer matches the current card's Turkish word.

        Args:
            selected_answer (str): The Turkish word selected by the user.

        Returns:
            bool: True if the selected answer is correct, False otherwise.
        """
        if self.current_card and selected_answer == self.current_card.turkish_word:
            self.update_score(True)
            return True
        return False

    def has_more_cards(self):
        """
        Checks if there are more cards to display.

        Returns:
            bool: True if more cards are available, False otherwise.
        """
        return len(self.flashcards) > 1

    def update_score(self, correct):
        """
        Updates the score if the user's answer is correct.

        Args:
            correct (bool): True if the user's answer is correct, False otherwise.
        """
        if correct:
            self.score += 1

    def reset_game(self):
        """
        Resets the game state, including score and flashcards.
        """
        self.score = 0
        self.current_card = None
        random.shuffle(self.flashcards)  # Optional: Shuffle flashcards for a fresh start
        self.next_card()

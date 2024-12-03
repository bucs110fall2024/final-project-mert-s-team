class Card:
    """
    A single flashcard with an English word and its Turkish translation pair.
    """

    def __init__(self, english_word, turkish_word):
        """
        Initializes a card object.

        Args:
            english_word (str): The word in English.
            turkish_word (str): The word's translation in Turkish.

        Raises:
            ValueError: If either english_word or turkish_word is not a string.
        """
        if not isinstance(english_word, str) or not isinstance(turkish_word, str):
            raise ValueError("Both english_word and turkish_word must be strings.")

        self.english_word = english_word
        self.turkish_word = turkish_word

    def check_answer(self, selected_word):
        """
        Checks if the selected word matches the Turkish translation.

        Args:
            selected_word (str): The word selected by the user.

        Returns:
            bool: True if the selected word matches the Turkish translation, False otherwise.
        """
        return selected_word == self.turkish_word
import pygame
from src.card import Card
from src.game_board import GameBoard


class Controller:
    """
    The Controller class handles the game logic, user input, and GUI rendering using Pygame.
    """

    def __init__(self):
        """
        Initializes the game, including setting up the screen, clock, and game board.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Turkish Flashcards Game")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_board = GameBoard()
        self.font = pygame.font.Font(None, 36)
        self.game_state = "START"  # Possible states: START, GAME, GAME_OVER
        self.feedback_message = ""
        self.feedback_timer = 0

        # Load flashcards from file
        try:
            self.game_board.load_flashcards("assets/flashcards.txt")
        except FileNotFoundError:
            print("Error: Flashcards file not found.")
            self.running = False

    def render_text(self, text, x, y, color=(0, 0, 0)):
        """
        Renders text on the screen.

        Args:
            text (str): The text to render.
            x (int): X-coordinate for the text position.
            y (int): Y-coordinate for the text position.
            color (tuple): RGB color of the text.
        """
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_start_screen(self):
        """
        Draws the start screen with a welcome message and instructions.
        """
        self.screen.fill((200, 200, 255))
        self.render_text("Welcome to the Turkish Flashcards Game!", 150, 200)
        self.render_text("Click anywhere to Start!", 250, 300)

    def draw_game_screen(self):
        """
        Draws the main game screen with the current flashcard, options, and score.
        """
        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Get the current card
        current_card = self.game_board.get_current_card()
        if current_card:
            # Display the word to translate
            self.render_text(f"Translate: {current_card.english_word}", 300, 50)
            # Display the player's current score
            self.render_text(f"Score: {self.game_board.score}", 650, 20)

            # Draw the answer options as buttons
            options = self.game_board.get_options()
            for i, option in enumerate(options):
                pygame.draw.rect(self.screen, (0, 255, 0), (150, 150 + i * 100, 500, 50))
                self.render_text(option, 180, 160 + i * 100)

            # Display feedback (e.g., "Correct!" or "Wrong!")
            if self.feedback_message:
                self.render_text(self.feedback_message, 300, 500, color=(255, 0, 0))
        else:
            # If no more cards are left, transition to the Game Over state
            self.game_state = "GAME_OVER"

    def draw_game_over_screen(self):
        """
        Draws the Game Over screen with the final score and restart instructions.
        """
        self.screen.fill((255, 200, 200))
        self.render_text("Game Over!", 300, 200)
        self.render_text(f"Your Final Score: {self.game_board.score}", 300, 300)
        self.render_text("Click to Restart or Close to Exit", 250, 400)

    def handle_click(self, x, y):
        """
        Handles mouse clicks based on the current game state.

        Args:
            x (int): X-coordinate of the mouse click.
            y (int): Y-coordinate of the mouse click.
        """
        if self.game_state == "START":
            # Transition from Start screen to Game screen
            self.game_state = "GAME"
        elif self.game_state == "GAME":
            # Only handle clicks on answer buttons
            button_y_positions = [150 + i * 100 for i in range(4)]
            for i, button_y in enumerate(button_y_positions):
                if 150 <= x <= 650 and button_y <= y <= button_y + 50:
                    # Get the selected option and check correctness
                    selected_option = self.game_board.get_options()[i]
                    is_correct = self.game_board.current_card.check_answer(selected_option)
                    self.game_board.update_score(is_correct)

                    # Show feedback for the answer
                    self.feedback_message = "Correct!" if is_correct else "Wrong!"
                    self.feedback_timer = 60  # Show feedback for 1 second (60 frames)

                    # Transition to the next card only after feedback is displayed
                    self.game_board.next_card()
                    break
        elif self.game_state == "GAME_OVER":
            # Restart the game when in Game Over state
            self.game_state = "START"
            self.game_board.reset_game()
            self.feedback_message = ""

    def mainloop(self):
        """
        Runs the main game loop, handling events, updating the game state, and rendering the GUI.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.handle_click(x, y)

            # Render the screen based on the current game state
            if self.game_state == "START":
                self.draw_start_screen()
            elif self.game_state == "GAME":
                self.draw_game_screen()
            elif self.game_state == "GAME_OVER":
                self.draw_game_over_screen()

            # Countdown feedback timer
            if self.feedback_timer > 0:
                self.feedback_timer -= 1
                if self.feedback_timer == 0:
                    self.feedback_message = ""

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
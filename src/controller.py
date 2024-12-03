import pygame
from src.card import Card
from src.game_board import GameBoard
import json


class Controller:
    def __init__(self):
        pygame.init()
        self.base_screen = pygame.display.set_mode((800, 600), pygame.SCALED)
        self.screen = pygame.Surface((800, 600))
        pygame.display.set_caption("Turkish Flashcards Game")

        self.COLORS = {
            'background': (245, 247, 250),
            'primary': (46, 196, 102),
            'secondary': (255, 255, 255),
            'text': (33, 33, 33),
            'accent': (70, 130, 240),
            'error': (255, 89, 89),
        }

        self.fonts = {
            'large': pygame.font.SysFont('Arial', 48),
            'medium': pygame.font.SysFont('Arial', 36),
            'small': pygame.font.SysFont('Arial', 24),
        }

        self.running = True
        self.clock = pygame.time.Clock()
        self.game_board = GameBoard()
        self.game_state = "USERNAME"  # Initial state
        self.feedback_message = ""
        self.feedback_timer = 0
        self.current_options = []
        self.username = ""
        self.high_scores = self.load_high_scores()
        self.button_hover = None

        try:
            self.game_board.load_flashcards("assets/flashcards.txt")
            self.current_options = self.game_board.get_options()
        except FileNotFoundError:
            print("Error: Flashcards file not found.")
            self.running = False

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_high_scores(self):
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)

    def update_high_score(self):
        if self.username not in self.high_scores or self.game_board.score > self.high_scores[self.username]:
            self.high_scores[self.username] = self.game_board.score
            self.save_high_scores()

    def render_text(self, text, size, x, y, color=None, centered=True):
        if color is None:
            color = self.COLORS['text']
        text_surface = self.fonts[size].render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y) if centered else (x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_username_screen(self):
        self.screen.fill(self.COLORS['background'])
        self.render_text("Enter Your Username", 'large', 400, 200)
        input_rect = pygame.Rect(250, 280, 300, 50)
        pygame.draw.rect(self.screen, self.COLORS['secondary'], input_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.COLORS['accent'], input_rect, 2, border_radius=10)
        self.render_text(self.username, 'medium', input_rect.centerx, input_rect.centery)
        self.render_text("Press Enter to continue", 'small', 400, 350)

    def draw_high_scores_screen(self):
        self.screen.fill(self.COLORS['background'])
        self.render_text("High Scores", 'large', 400, 100)
        y_pos = 200
        sorted_scores = sorted(self.high_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (username, score) in enumerate(sorted_scores[:10]):  # Show top 10
            self.render_text(f"{i + 1}. {username}: {score}", 'medium', 400, y_pos)
            y_pos += 40
        self.render_text("Press ESC to return to the menu", 'small', 400, 550)

    def draw_game_screen(self):
        self.screen.fill(self.COLORS['background'])
        current_card = self.game_board.get_current_card()

        if current_card:
            pygame.draw.rect(self.screen, self.COLORS['secondary'], (0, 0, 800, 100))
            self.render_text(f"Translate: {current_card.english_word}", 'large', 400, 50)
            score_text = f"Score: {self.game_board.score}"
            pygame.draw.rect(self.screen, self.COLORS['accent'], (680, 20, 100, 40), border_radius=10)
            self.render_text(score_text, 'medium', 730, 40, self.COLORS['secondary'])
            self.render_text(f"Player: {self.username}", 'small', 100, 30, centered=False)

            if self.feedback_message:
                color = self.COLORS['primary'] if "Correct" in self.feedback_message else self.COLORS['error']
                self.render_text(self.feedback_message, 'medium', 400, 110, color)

            button_height = 80
            spacing = 20
            start_y = 200

            for i, option in enumerate(self.current_options):
                button_rect = pygame.Rect(150, start_y + i * (button_height + spacing), 500, button_height)
                is_hovered = self.button_hover == i
                pygame.draw.rect(self.screen, 
                               self.COLORS['secondary'] if is_hovered else self.COLORS['primary'],
                               button_rect, border_radius=10)
                self.render_text(option, 'medium', button_rect.centerx, button_rect.centery,
                               self.COLORS['text'] if is_hovered else self.COLORS['secondary'])

    def handle_username_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.username.strip():
                self.game_state = "GAME"
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif len(self.username) < 15 and event.unicode.isprintable():
                self.username += event.unicode

    def handle_game_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_height = 80
            spacing = 20
            start_y = 200

            for i, _ in enumerate(self.current_options):
                button_rect = pygame.Rect(150, start_y + i * (button_height + spacing), 500, button_height)
                if button_rect.collidepoint(mouse_pos):
                    is_correct = self.game_board.check_answer(self.current_options[i])
                    self.feedback_message = "Correct!" if is_correct else "Incorrect!"
                    self.feedback_timer = 60

                    if self.game_board.has_more_cards():
                        self.current_options = self.game_board.get_options()
                    else:
                        self.update_high_score()
                        self.game_state = "GAME_OVER"
                    break

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.game_state == "USERNAME":
                    self.handle_username_input(event)
                elif self.game_state == "GAME":
                    self.handle_game_input(event)

            if self.game_state == "USERNAME":
                self.draw_username_screen()
            elif self.game_state == "GAME":
                self.draw_game_screen()

            self.base_screen.blit(pygame.transform.scale(self.screen, (800, 600)), (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

import pygame
from src.card import Card
from src.game_board import GameBoard

class Controller:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Turkish Flashcards Game")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_board = GameBoard()
        self.font = pygame.font.Font(None, 36)
        self.game_board.load_flashcards("assets/flashcards.txt")

    def render_text(self, text, x, y, color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_screen(self):
        self.screen.fill((255, 255, 255))
        current_card = self.game_board.get_current_card()
        self.render_text(f"Translate: {current_card.english_word}", 300, 50)
        self.render_text(f"Score: {self.game_board.score}", 650, 20)
        button_texts = self.game_board.get_options()
        for i, text in enumerate(button_texts):
            pygame.draw.rect(self.screen, (0, 255, 0), (150, 150 + i * 100, 500, 50))
            self.render_text(text, 180, 160 + i * 100)

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.handle_click(x, y)

            self.draw_screen()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_click(self, x, y):
        button_y_positions = [150 + i * 100 for i in range(4)]
        for i, button_y in enumerate(button_y_positions):
            if 150 <= x <= 650 and button_y <= y <= button_y + 50:
                selected_option = self.game_board.get_options()[i]
                is_correct = self.game_board.current_card.check_answer(selected_option)
                self.game_board.update_score(is_correct)
                self.game_board.next_card()
                break

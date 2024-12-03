import pygame
from src.card import Card
from src.game_board import GameBoard

class Controller:
    """
    Enhanced Controller class with improved UI design and animations
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Turkish Flashcards Game")
        
        self.COLORS = {
            'background': (245, 247, 250),
            'primary': (46, 196, 102),
            'secondary': (255, 255, 255),
            'text': (33, 33, 33),
            'accent': (70, 130, 240),
            'error': (255, 89, 89)
        }
        
        self.fonts = {
            'large': pygame.font.Font(None, 48),
            'medium': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 24)
        }
        
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_board = GameBoard()
        self.game_state = "START"
        self.feedback_message = ""
        self.feedback_timer = 0
        self.current_options = []
        
        # Animation variables
        self.button_hover = None
        self.transition_alpha = 255
        self.is_transitioning = False
        
        # Load flashcards
        try:
            self.game_board.load_flashcards("assets/flashcards.txt")
            if self.game_board.get_current_card():
                self.current_options = self.game_board.get_options()
        except FileNotFoundError:
            print("Error: Flashcards file not found.")
            self.running = False

    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def render_text(self, text, font_size, x, y, color=None, centered=True):
        """Enhanced text rendering with multiple font sizes and centering"""
        if color is None:
            color = self.COLORS['text']
        font = self.fonts[font_size]
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_button(self, text, x, y, width, height, hover=False):
        """Draw an animated button with hover effects"""
        button_rect = pygame.Rect(x, y, width, height)
        color = self.COLORS['primary'] if hover else self.COLORS['secondary']
        
        # Draw button shadow
        shadow_rect = button_rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 30), shadow_rect, border_radius=10)
        
        # Draw main button
        self.draw_rounded_rect(self.screen, color, button_rect, 10)
        
        # Draw button text
        text_color = self.COLORS['secondary'] if hover else self.COLORS['text']
        self.render_text(text, 'medium', x + width//2, y + height//2, text_color)
        
        return button_rect

    def draw_start_screen(self):
        """Enhanced start screen with animations"""
        self.screen.fill(self.COLORS['background'])
        
        # Draw title with shadow effect
        title = "Turkish Flashcards"
        shadow_offset = 2
        self.render_text(title, 'large', 402, 202, (0, 0, 0, 50))
        self.render_text(title, 'large', 400, 200, self.COLORS['accent'])
        
        # Animated start button
        self.draw_button("Start Game", 300, 300, 200, 50, 
                         self.button_hover == "start")

    def draw_game_screen(self):
        """Enhanced game screen with modern UI elements"""
        self.screen.fill(self.COLORS['background'])
        current_card = self.game_board.get_current_card()
        
        if current_card:
            # Draw header bar
            pygame.draw.rect(self.screen, self.COLORS['secondary'], 
                             (0, 0, 800, 100))
            
            # Draw word to translate
            self.render_text(f"{current_card.english_word}", 'large', 
                             400, 50, self.COLORS['text'])
            
            # Draw score
            score_text = f"Score: {self.game_board.score}"
            self.render_text(score_text, 'medium', 650, 30, 
                             self.COLORS['accent'], centered=False)
            
            # Draw answer options
            button_height = 80
            spacing = 20
            total_height = (button_height + spacing) * len(self.current_options)
            start_y = (600 - total_height) // 2
            
            for i, option in enumerate(self.current_options):
                y_pos = start_y + i * (button_height + spacing)
                self.draw_button(option, 150, y_pos, 500, button_height,
                                 self.button_hover == i)

            # Draw feedback message
            if self.feedback_message:
                color = self.COLORS['primary'] if "Correct" in self.feedback_message \
                    else self.COLORS['error']
                self.render_text(self.feedback_message, 'medium', 400, 550, color)

    def handle_click(self, x, y, event_type=pygame.MOUSEBUTTONDOWN):
        """Enhanced click handling with button feedback"""
        if event_type != pygame.MOUSEBUTTONDOWN:
            return

        if self.game_state == "START":
            if 300 <= x <= 500 and 300 <= y <= 350:
                self.game_state = "GAME"
                self.current_options = self.game_board.get_options()
                self.transition_alpha = 255
                self.is_transitioning = True
                
        elif self.game_state == "GAME":
            button_height = 80
            spacing = 20
            total_height = (button_height + spacing) * len(self.current_options)
            start_y = (600 - total_height) // 2
            
            for i in range(len(self.current_options)):
                y_pos = start_y + i * (button_height + spacing)
                if 150 <= x <= 650 and y_pos <= y <= y_pos + button_height:
                    selected_option = self.current_options[i]
                    is_correct = self.game_board.current_card.check_answer(selected_option)
                    self.game_board.update_score(is_correct)
                    
                    self.feedback_message = "Correct!" if is_correct else "Wrong!"
                    self.feedback_timer = 60
                    
                    self.game_board.next_card()
                    self.current_options = self.game_board.get_options()
                    break
                    
        elif self.game_state == "GAME_OVER":
            if 300 <= x <= 500 and 400 <= y <= 450:
                self.game_state = "START"
                self.game_board.reset_game()
                self.feedback_message = ""
                self.current_options = self.game_board.get_options()

    def update_hover_state(self, x, y):
        """Update button hover states for animations"""
        self.button_hover = None
        
        if self.game_state == "START":
            if 300 <= x <= 500 and 300 <= y <= 350:
                self.button_hover = "start"
                
        elif self.game_state == "GAME":
            button_height = 80
            spacing = 20
            total_height = (button_height + spacing) * len(self.current_options)
            start_y = (600 - total_height) // 2
            
            for i in range(len(self.current_options)):
                y_pos = start_y + i * (button_height + spacing)
                if 150 <= x <= 650 and y_pos <= y <= y_pos + button_height:
                    self.button_hover = i
                    break

    def mainloop(self):
        """Enhanced main loop with smooth animations"""
        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update_hover_state(mouse_x, mouse_y)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button only
                        self.handle_click(mouse_x, mouse_y, event.type)

            if self.game_state == "START":
                self.draw_start_screen()
            elif self.game_state == "GAME":
                self.draw_game_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

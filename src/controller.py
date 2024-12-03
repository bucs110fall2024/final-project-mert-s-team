import pygame
from src.card import Card
from src.game_board import GameBoard

class Controller:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Turkish Flashcards Game")
        
        # Initialize colors
        self.COLORS = {
            'background': (245, 247, 250),
            'primary': (46, 196, 102),
            'secondary': (255, 255, 255),
            'text': (33, 33, 33),
            'accent': (70, 130, 240),
            'error': (255, 89, 89),
            'input_bg': (255, 255, 255),
            'input_border': (200, 200, 200)
        }
        
        # Initialize fonts
        self.fonts = {
            'large': pygame.font.Font(None, 48),
            'medium': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 24)
        }
        
        # Initialize game state variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_board = GameBoard()
        self.game_state = "USERNAME"  # Initial state
        self.feedback_message = ""
        self.feedback_timer = 0
        self.current_options = []
        
        # Username related variables
        self.username = ""
        self.username_active = True
        self.max_username_length = 15
        self.username_cursor_visible = True
        self.username_cursor_timer = 0
        
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

    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

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

    def draw_username_screen(self):
        """Draw the username input screen"""
        self.screen.fill(self.COLORS['background'])
        
        # Draw title
        self.render_text("Enter Your Username", 'large', 400, 150, self.COLORS['accent'])
        
        # Draw input box
        input_rect = pygame.Rect(250, 250, 300, 50)
        pygame.draw.rect(self.screen, self.COLORS['input_bg'], input_rect)
        pygame.draw.rect(self.screen, self.COLORS['input_border'], input_rect, 2)
        
        # Draw username text with cursor
        display_text = self.username
        if self.username_active and self.username_cursor_visible:
            display_text += "|"
        
        text_surface = self.fonts['medium'].render(display_text, True, self.COLORS['text'])
        text_rect = text_surface.get_rect(center=input_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Draw continue button if username is not empty
        if self.username:
            self.draw_button("Continue", 300, 350, 200, 50, self.button_hover == "continue")

    def draw_game_screen(self):
        """Enhanced game screen with username display"""
        self.screen.fill(self.COLORS['background'])
        current_card = self.game_board.get_current_card()
        
        if current_card:
            # Draw header bar
            pygame.draw.rect(self.screen, self.COLORS['secondary'], (0, 0, 800, 100))
            
            # Draw username
            self.render_text(f"Player: {self.username}", 'small', 100, 30, 
                           self.COLORS['accent'], centered=False)
            
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

    def handle_username_input(self, event):
        """Handle username input events"""
        if event.type == pygame.KEYDOWN and self.username_active:
            if event.key == pygame.K_RETURN and self.username:
                self.game_state = "START"
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif len(self.username) < self.max_username_length and event.unicode.isprintable():
                self.username += event.unicode

    def handle_start_screen_input(self, event):
        """Handle start screen input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter key pressed
                self.game_state = "GAME"
                self.current_options = self.game_board.get_options()
                self.transition_alpha = 255
                self.is_transitioning = True

    def handle_click(self, x, y, event_type=pygame.MOUSEBUTTONDOWN):
        """Enhanced click handling with username screen"""
        if event_type != pygame.MOUSEBUTTONDOWN:
            return

        if self.game_state == "USERNAME":
            # Check if continue button is clicked
            if self.username and 300 <= x <= 500 and 350 <= y <= 400:
                self.game_state = "START"
                
        elif self.game_state == "START":
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

    def update_hover_state(self, x, y):
        """Update button hover states for animations"""
        self.button_hover = None
        
        if self.game_state == "USERNAME":
            if self.username and 300 <= x <= 500 and 350 <= y <= 400:
                self.button_hover = "continue"
        
        elif self.game_state == "START":
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
        """Enhanced main loop with keyboard input handling"""
        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update_hover_state(mouse_x, mouse_y)
            
            # Update username cursor blink
            self.username_cursor_timer += 1
            if self.username_cursor_timer >= 30:  # Blink every 30 frames
                self.username_cursor_visible = not self.username_cursor_visible
                self.username_cursor_timer = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button only
                        self.handle_click(mouse_x, mouse_y, event.type)
                elif self.game_state == "USERNAME":
                    self.handle_username_input(event)
                elif self.game_state == "START":
                    self.handle_start_screen_input(event)

            if self.game_state == "USERNAME":
                self.draw_username_screen()
            elif self.game_state == "START":
                self.draw_start_screen()
            elif self.game_state == "GAME":
                self.draw_game_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
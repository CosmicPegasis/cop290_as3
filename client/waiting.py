from menu import Menu
import main_menu
import room
from constants import BLACK, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH, SELECTED_COLOR
import pygame

class Waiting(Menu):
    def __init__(self):
        self.helper()
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = []
        self.game_type = "versus_waiting"
        print(self.game_type)
        

    def update(self):
        pass
    
    def helper(self):
        
        self.game_type = "versus_waiting"
        

    def handle_selection(self, selected_option):
        
        return True
    
    def render(self, window):
        window.fill(BLACK)
        
        score_font = pygame.font.Font(None, 48) 
        score_text = score_font.render("Waiting for Player...", True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (WINDOW_WIDTH // 2, 50) 
        window.blit(score_text, score_text_rect)

        for i, option in enumerate(self.OPTIONS):
            if i == self.selected_option:
                color = SELECTED_COLOR
            else:
                color = WHITE

            text = self.font.render(option, True, color)
            text_rect = text.get_rect()
            text_rect.midtop = (
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 - len(self.OPTIONS) * 36 // 2 + i * 36,
            )
            window.blit(text, text_rect)

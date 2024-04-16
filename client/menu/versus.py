from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.waiting as waiting
import pygame
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class Versus(Menu):
    def __init__(self, message=None):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Find Match", "Back"]
        self.message = message
        self.asset_man.load_sound("find_match", "assets/versus/find_match.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.switch_screen = True
            self.new_screen = waiting.Waiting()
            pygame.mixer.music.pause()
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()
        return True

    def render(self, window):
        window.fill(BLACK)
        if self.message:
            score_font = pygame.font.Font(None, 48)
            score_text = score_font.render(self.message, True, WHITE)
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

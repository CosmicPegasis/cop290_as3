from client.menu.menu import Menu
import client.games.base_game as base_game
import pygame
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class MultiGame(Menu):
    def __init__(self, p):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = []
        self.flag = 0

        self.game_screen = base_game.MidiGame("assets/midi/happy_birthday.mid", 4)
        self.asset_man.load_sound("halt", "assets/multiplayer_game/halt.mp3")
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.player_id = p

        self.game_type = "versus_act_mult_game"
        self.score = 0
        self.halt_flag =0 

    def start_game(self):
        if self.flag == 0:
            self.game_screen.start()
            self.flag = 1

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.halt_flag =1
        return True

    def render(self, window):
        window.fill(BLACK)
        score_font = pygame.font.Font(None, 48)

        score_text = score_font.render("Player-" + str(self.player_id), True, WHITE)

        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        window.blit(score_text, score_text_rect)     
        text = self.font.render("Press 'Enter' to end the game", True, WHITE)
        text_rect = text.get_rect()
        text_rect.midtop = (
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 1 * 36 // 2 + 0 * 36,
        )
        window.blit(text, text_rect)

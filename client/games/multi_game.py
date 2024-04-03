from client.menu.menu import Menu
import client.menu.single_player as single_player
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

        self.game_screen = base_game.BaseGame("assets/midi/happy_birthday.mid", 4)
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.player_id = p

        self.game_type = "versus_act_mult_game"
        self.score = 0

    def start_game(self):
        if self.flag == 0:
            # self.play_sound("the_game_starts_in")
            # time.sleep(1)
            # self.play_sound("3")
            # time.sleep(1)
            # self.play_sound("2")
            # time.sleep(1)
            # self.play_sound("1")
            # time.sleep(1)
            # self.flag =1

            self.game_screen.start()
            self.flag = 1

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.game_screen.stop()
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()

        return True

    def render(self, window):
        window.fill(BLACK)
        score_font = pygame.font.Font(None, 48)

        score_text = score_font.render("Player-" + str(self.player_id), True, WHITE)

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

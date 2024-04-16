from client.menu.menu import Menu
import client.menu.battle_mode as battle
import client.menu.waiting_battle as waiting

from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import pygame
import time


class BattleResults(Menu):
    def __init__(self, move1, move2, player_id):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Play Again", "Back"]

        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")

        self.asset_man.load_sound("back", "assets/back.mp3")
        self.move1 = move1
        self.move2 = move2
        self.player_id = player_id
        self.game_type == "battle_results"
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.asset_man.load_sound("oppo_score_is", "assets/pitch/oppo_score_is.mp3")
        # time.sleep(1)
        # self.play_sound("your_score_is")
        # time.sleep(2)
        # self.load_score(move1)
        # time.sleep(1)
        # self.play_sound("oppo_score_is")
        # time.sleep(2)
        # self.load_score(move2)

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.switch_screen = True
            self.new_screen = waiting.Waiting_Battle()
            pygame.mixer.music.pause()
        else:
            self.switch_screen = True
            self.new_screen = battle.Battle()
        return True

    def load_score(self, score):

        str_form = str(score)

        for digit in str_form:
            time.sleep(0.3)
            path_sd = "assets/numbers/" + digit + ".mp3"
            time.sleep(0.3)
            self.asset_man.load_sound(digit, path_sd)
            self.play_sound(digit)

    def render(self, window):
        window.fill(BLACK)

        score_font = pygame.font.Font(None, 48)
        if self.player_id == 0:
            score_text = score_font.render(
                "Your " + "score: " + str(self.move1),
                True,
                WHITE,
            )
            opponent_text = score_font.render(
                "Opponent's score: " + str(self.move2),
                True,
                WHITE,
            )
        else:
            score_text = score_font.render(
                "Your " + "score: " + str(self.move2),
                True,
                WHITE,
            )
            opponent_text = score_font.render(
                "Opponent's score: " + str(self.move1),
                True,
                WHITE,
            )
        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (WINDOW_WIDTH // 2, 50)
        opponent_text_rect = opponent_text.get_rect()
        opponent_text_rect.midtop = (WINDOW_WIDTH // 2, 125)
        window.blit(score_text, score_text_rect)
        window.blit(opponent_text, opponent_text_rect)

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

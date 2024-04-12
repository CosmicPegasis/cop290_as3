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


class BattleResults(Menu):
    def __init__(self, move1, move2, player_id):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Play Again", "Back"]

        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.move1 = move1
        self.move2 = move2
        self.player_id = player_id

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

    def render(self, window):
        window.fill(BLACK)

        score_font = pygame.font.Font(None, 48)
        if self.player_id == 0:
            score_text = score_font.render(
                "You are Player "
                + str(self.player_id)
                + " score is "
                + str(self.move1)
                + "/"
                + str(self.move2),
                True,
                WHITE,
            )
        else:
           score_text = score_font.render(
                "You are Player "
                + str(self.player_id)
                + " score is "
                + str(self.move2)
                + "/"
                + str(self.move1),
                True,
                WHITE,
            )
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

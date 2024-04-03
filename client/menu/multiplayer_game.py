from client.menu.menu import Menu
import client.menu.versus as versus
from client.constants import BLACK, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH, SELECTED_COLOR
import pygame


class MultiplayerGame(Menu):
    def __init__(self, move1, move2, player_id):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Play Again", "Change Opponent", "Back"]

        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        self.asset_man.load_sound(
            "change_opponent", "assets/multiplayer_game/change_opponent.mp3"
        )
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.move1 = move1
        self.move2 = move2
        self.player_id = player_id

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            pass
        elif selected_option == 1:
            self.switch_screen = True
            # TODO Add change opponent functionality (To be done in client-server system)
        else:
            self.switch_screen = True
            self.new_screen = versus.Versus()
        return True

    def render(self, window):
        window.fill(BLACK)

        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(
            "You are Player "
            + str(self.player_id)
            + " score is "
            + self.move1
            + "/"
            + self.move2,
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

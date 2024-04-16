from client.menu.menu import Menu
import pygame
import client.games.practice_game as practice_pitch
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)
import client.menu.practice_para as parameter_parameter_pitch


class PracticeResults(Menu):
    def __init__(self, score,narrate_name,narrate_pitch,note_length):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Info", "Play Again", "Back"]
        pygame.mixer.music.pause()
        self.asset_man.load_sound("your_score_is", "assets/pitch/your_score_is.mp3")
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.score = score
        self.narrate_name = narrate_name
        self.narrate_pitch = narrate_pitch
        self.note_length = note_length
        time.sleep(1)
        self.play_sound("your_score_is")
        time.sleep(2)
        self.load_score(score)

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            print("This is info.")
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = practice_pitch.Practice_game(self.narrate_name,self.narrate_pitch,self.note_length)
            pygame.mixer.music.pause()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = parameter_parameter_pitch.Parameters_practice(self.narrate_name,self.narrate_pitch,self.note_length,-1)
            pygame.mixer.music.pause()
        return True

    def load_score(self, score):
        pygame.mixer.music.pause()
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
        score_text = score_font.render("Your score is " + str(self.score), True, WHITE)
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

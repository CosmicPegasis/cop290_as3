from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.pitch_results as pitch_results
import client.pitch as pitch
import client.practice as practice
import client.menu.songs as songs
import pygame
import client.game as game
import time


class SinglePlayer(Menu):
    def __init__(self):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Info", "Pitch", "Songs", "Practice", "Back"]
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("pitch", "assets/single/pitch.mp3")
        self.asset_man.load_sound("songs", "assets/single/songs.mp3")
        self.asset_man.load_sound("practice", "assets/single/practice.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("info_menu", "assets/menu/info_menu.mp3")
        self.asset_man.load_sound("count_down", "assets/count_down.mp3")
        self.info_sound_playing = False
        self.score = 0

    def update(self):
        pass

    # TODO Pause background music (Done)
    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.play_info_sound()
        elif selected_option == 1:

            self.switch_screen = True
            self.new_screen = pitch.Pitch()
            pygame.mixer.music.pause()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = songs.Songs()
        elif selected_option == 3:

            self.switch_screen = True
            self.new_screen = practice.Practice()
        else:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()

        return True

    def play_info_sound(self):
        self.play_sound("info_menu")
        self.info_sound_playing = True

    def stop_info_sound(self):
        self.asset_man.sounds["info_menu"].stop()
        self.info_sound_playing = False

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.info_sound_playing:
                    self.stop_info_sound()

        return super().handle_events(events)

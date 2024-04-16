from client.menu.menu import Menu
import client.menu.single_player as single_player
import client.menu.songs_parameter as songs_parameter
import pygame


class SongsMenu(Menu):
    def __init__(self):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Happy Birthday", "Twinkle", "back"]

        self.asset_man.load_sound(
            "happy_birthday", "assets/songs_menu/happy_birthday.mp3"
        )
        self.asset_man.load_sound("twinkle", "assets/songs_menu/twinkle.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == len(self.OPTIONS) - 1:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()
        else:
            self.switch_screen = True
            self.new_screen = songs_parameter.SongsParameters(
                self.OPTIONS[selected_option], True, True, 3, -1
            )
            pygame.mixer.music.pause()

        return True

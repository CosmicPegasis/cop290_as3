from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.waiting_battle as waiting
import pygame


class Battle(Menu):
    def __init__(self):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Find Match", "Back"]
        
        self.asset_man.load_sound("find_match", "assets/versus/find_match.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.switch_screen = True
            self.new_screen = waiting.Waiting_Battle()
            pygame.mixer.music.pause()
        if selected_option == 1:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()
        return True

from main_menu import MainMenu
from game import Game


class ScreenManager:
    def __init__(self, asset_manager, audio_manager):
        self.asset_manager = asset_manager
        self.audio_manager = audio_manager
        self.screens = {
            "main_menu": MainMenu(asset_manager, audio_manager),
            "game": Game(asset_manager, audio_manager),
            # Add more screens here
        }
        self.current_screen = self.screens["main_menu"]

    def switch_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

from menu import Menu
import main_menu


class SinglePlayer(Menu):
    def __init__(self):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Pitch", "Songs", "Back"]

        self.asset_man.load_sound("pitch", "assets/single/pitch.mp3")
        self.asset_man.load_sound("songs", "assets/single/songs.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            print("Starting a new game...")
        elif selected_option == 1:
            print("Starting a new game...")
        else:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()
        return True

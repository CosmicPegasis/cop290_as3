from menu import Menu
import single_player

class Practice(Menu):
    def __init__(self):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Play Again","Back"]

        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.new_screen = single_player.SinglePlayer()
            self.new_screen.handle_selection(2)
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()
        return True

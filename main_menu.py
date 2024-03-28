from menu import Menu
import versus
import single_player


class MainMenu(Menu):
    def __init__(self):
        super().__init__("assets/menu/background.mp3")
        self.OPTIONS = ["Single Player", "Versus Mode", "Exit"]

        self.asset_man.load_sound("single_player", "assets/menu/single_player.mp3")
        self.asset_man.load_sound("versus_mode", "assets/menu/versus_mode.mp3")
        self.asset_man.load_sound("exit", "assets/menu/exit.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = versus.Versus()
        elif selected_option == 2:
            return False

        return True

from client.menu.menu import Menu
import client.menu.versus as versus
import client.menu.multiplayer_game as multiplayer_game


class Room(Menu):
    def __init__(self):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Ready", "Back"]

        self.asset_man.load_sound("ready", "assets/room/ready.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            print("Ready")
            self.switch_screen = True
            self.new_screen = multiplayer_game.MultiplayerGame()
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = versus.Versus()

        return True

from menu import Menu
import room
import versus

class MultiplayerGame(Menu):
    def __init__(self):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Play Again","Change Opponent","Back"]

        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        self.asset_man.load_sound("change_opponent", "assets/multiplayer_game/change_opponent.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.new_screen = room.Room()
            room.Room.handle_selection(self.new_screen,0)
        elif selected_option == 1:
            self.switch_screen = True
            # TODO Add change opponent functionality
            self.new_screen = room.Room()
        else:
            self.switch_screen = True
            self.new_screen = versus.Versus()
        return True

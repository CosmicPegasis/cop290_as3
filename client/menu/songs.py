from client.menu.menu import Menu
import client.menu.single_player as single_player
import client.menu.song_menu as song_menu


class Songs(Menu):
    def __init__(self):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["back", "back", "back", "back", "back"]

        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == len(self.OPTIONS) - 1:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()
        else:
            print("starting a new game with song-", selected_option)
            self.switch_screen = True
            self.new_screen = song_menu.SongResultMenu(selected_option)

        return True

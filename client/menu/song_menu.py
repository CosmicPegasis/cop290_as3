from client.menu.menu import Menu
import client.menu.songs as songs


class SongResultMenu(Menu):
    def __init__(self, song_number):
        super().__init__("assets/versus/background.mp3")
        self.OPTIONS = ["Play Again", "Back"]
        self.song_number = song_number
        self.asset_man.load_sound("play_again", "assets/pitch/play_again.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")

    def update(self):
        pass

    def handle_selection(self, selected_option):
        if selected_option == 0:
            self.new_screen = songs.Songs()
            songs.Songs.handle_selection(self.new_screen, self.song_number)
        elif selected_option == 1:
            self.switch_screen = True
            self.new_screen = songs.Songs()
        return True

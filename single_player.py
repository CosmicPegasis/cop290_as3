from menu import Menu
import main_menu
import pitch_results
import practice
import songs
import pygame
import game
import time

class SinglePlayer(Menu):
    def __init__(self):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Info","Pitch", "Songs","Practice", "Back"]
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("pitch", "assets/single/pitch.mp3")
        self.asset_man.load_sound("songs", "assets/single/songs.mp3")
        self.asset_man.load_sound("practice", "assets/single/practice.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        self.asset_man.load_sound("info_menu", "assets/menu/info_menu.mp3")
        self.asset_man.load_sound("count_down","assets/count_down.mp3")
        self.info_sound_playing = False

    def update(self):
        pass

    # TODO Pause background music
    def handle_selection(self, selected_option):
        if selected_option ==0:
            self.play_info_sound()
        elif selected_option == 1:
            print("Starting a new pitch game...")
            print("Game has been finished.")
            print("------------------------")
            self.play_sound("count_down")
            # TODO fix time delay
            time.sleep(4)
            game.game_funct("assets/midi/happy_birthday.mid", 4)
            self.switch_screen = True
            self.new_screen = pitch_results.PitchResultMenu()
        elif selected_option == 2:
            self.switch_screen = True
            self.new_screen = songs.Songs()
        elif selected_option == 3:
            print("Starting a new practice game...")
            print("Game has been finished.")
            print("------------------------")
            self.switch_screen = True
            self.new_screen = practice.Practice()
        else:
            self.switch_screen = True
            self.new_screen = main_menu.MainMenu()
        
        return True
    
    def play_info_sound(self):
        self.play_sound("info_menu")
        self.info_sound_playing = True
        
    def stop_info_sound(self):
        self.asset_man.sounds["info_menu"].stop()
        self.info_sound_playing = False
        
    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.info_sound_playing:
                    self.stop_info_sound()
            
        return super().handle_events(events)

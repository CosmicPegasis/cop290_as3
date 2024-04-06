from client.menu.menu import Menu
import client.menu.main_menu as main_menu
import client.menu.pitch_results as pitch_results
import client.games.learn_pitch as learn_pitch
import client.games.practice_results as practice_results

import pygame
import client.games.base_game as base_game
import client.menu.single_player as single_player
import time
from client.utils.constants import (
    BLACK,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SELECTED_COLOR,
)


class Parameters(Menu):
    def __init__(self,narrate_name,narrate_pitch,note_length,selected_option):
        super().__init__("assets/single/background.mp3")
        self.OPTIONS = ["Narrate name", "Narrate pitch", "Note length","Play", "Back"]
        self.asset_man.load_sound("info", "assets/info.mp3")
        self.asset_man.load_sound("narrate_name", "assets/parameters/narrate_name.mp3")
        self.asset_man.load_sound("narrate_pitch", "assets/parameters/narrate_pitch.mp3")
        self.asset_man.load_sound("note_length", "assets/parameters/note_length.mp3")
        self.asset_man.load_sound("play","assets/home/play.mp3")
        self.asset_man.load_sound("back", "assets/back.mp3")
        
        self.asset_man.load_sound("count_down", "assets/count_down.mp3")
        self.info_sound_playing = False
        self.score = 0
        self.selected_option = selected_option
        
        self.narrate_name = narrate_name
        self.narrate_pitch = narrate_pitch
        self.note_length = note_length

    def update(self):
        pass

    # TODO Pause background music (Done)
    def handle_selection(self, selected_option):
        
        if selected_option == 0:
            self.narrate_name = not(self.narrate_name)
            self.switch_screen = True
            self.new_screen = Parameters(self.narrate_name,self.narrate_pitch,self.note_length,selected_option)
            # self.switch_screen = True
            # self.new_screen = learn_pitch.LearnPitch()
            # pygame.mixer.music.pause()
        elif selected_option == 1:
            self.narrate_pitch = not(self.narrate_pitch)
            self.switch_screen = True
            self.new_screen = Parameters(self.narrate_name,self.narrate_pitch,self.note_length,selected_option)
        elif selected_option == 2:
            self.note_length = self.note_length+1
            self.switch_screen = True
            self.new_screen = Parameters(self.narrate_name,self.narrate_pitch,self.note_length,selected_option)
        elif selected_option == 3:
            self.switch_screen = True
            self.new_screen = learn_pitch.LearnPitch(self.narrate_name,self.narrate_pitch,self.note_length)
            pygame.mixer.music.pause()
        else:
            self.switch_screen = True
            self.new_screen = single_player.SinglePlayer()

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
    
    def render(self, window):
        window.fill(BLACK)

        

        for i, option in enumerate(self.OPTIONS):
            if i == self.selected_option:
                color = SELECTED_COLOR
            else:
                color = WHITE
            
            if i==0:
                value = "OFF"
                if self.narrate_name == True:
                    value = "ON"
                text = self.font.render(option+ " - "+value, True, color)
            elif i == 1:
                value = "OFF"
                if self.narrate_pitch == True:
                    value = "ON"
                text = self.font.render(option+" - "+value,True,color)
            elif i == 2:
                value = str(self.note_length)
                text = self.font.render(option+" - "+value,True,color)
            else:
                text = self.font.render(option,True,color)
                
            
            

            
            text_rect = text.get_rect()
            text_rect.midtop = (
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 - len(self.OPTIONS) * 36 // 2 + i * 36,
            )
            window.blit(text, text_rect)
            
    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                prev_selected_option = self.selected_option

                if event.key == pygame.K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = min(
                        len(self.OPTIONS) - 1, self.selected_option + 1
                    )
                elif event.key == pygame.K_RETURN:
                    if self.selected_option !=2: 
                        if not self.handle_selection(self.selected_option):
                            return False
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option == 2:
                        self.note_length = self.note_length+1
                        self.switch_screen = True
                        self.new_screen = Parameters(self.narrate_name,self.narrate_pitch,self.note_length,self.selected_option)
                        return True
                        
                elif event.key == pygame.K_LEFT:
                    if self.selected_option == 2:
                        self.note_length = max(0,self.note_length-1)
                        self.switch_screen = True
                        self.new_screen = Parameters(self.narrate_name,self.narrate_pitch,self.note_length,self.selected_option)
                        return True
                        
                if self.selected_option != prev_selected_option:
                    self.play_sound("click")
                    self.play_sound(
                        self.OPTIONS[self.selected_option].lower().replace(" ", "_")
                    )

        return True

            
        


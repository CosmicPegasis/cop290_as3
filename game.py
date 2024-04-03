import pygame
import pygame.midi
from midi_play import get_midi_file_events
from score import calc_score
import midi_play
import menu



class MidiGame:
    def __init__(self, midi_file_path, note_length):
        self.midi_file = midi_file_path
        self.cur_events = []
        self.clock = pygame.time.Clock()
        self.midi_narrator = midi_play.MidiNarrator(self.midi_file, note_length)
        self.note_length = note_length
        
       
        
        pygame.midi.init()
        self.input_id = pygame.midi.get_default_input_id()
        if self.input_id == -1:
            print("No MIDI input devices found.")
            exit()

        self.midi_input = pygame.midi.Input(self.input_id)
        self.output_id = 0
        for i in range(pygame.midi.get_count()):
            print(pygame.midi.get_device_info(i))
            if pygame.midi.get_device_info(i)[1] == b"Microsoft GS Wavetable Synth":
               self.output_id = i

        self.midi_output = pygame.midi.Output(2)

    def is_running(self):
        return self.midi_narrator.is_playing()

    def start(self):
        self.midi_narrator.play()

    def handle_events(self):
        
        if self.midi_input.poll():
            midi_events = self.midi_input.read(10)
            midi_evs = pygame.midi.midis2events(midi_events, self.midi_input.device_id)
            for event in midi_evs:
                if event.type == pygame.midi.MIDIIN:
                    print(event)
                    note, velocity = event.data1, event.data2
                    if velocity > 0:
                        self.midi_output.note_on(note, velocity)
                        self.cur_events.append(['on', note, event.timestamp])
                    else:
                        self.midi_output.note_off(note)
                        self.cur_events.append(['off', note, event.timestamp])

    # TODO Fix midi
    def stop(self):
        pygame.mixer.music.pause()
        self.midi_narrator.stop_playback()
        reference = get_midi_file_events(self.midi_file)
        pygame.midi.quit()
        return calc_score(self.cur_events, reference, self.note_length)

# TODO Do not use game_funct
# def game_funct(song_name,speed):
#     game = MidiGame(song_name, speed)  
    
#     game.start()
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event == pygame.QUIT:
#                 running = False
#         game.handle_events() 
#         if not game.is_running():
#             print(game.stop())
#             running = False
            

if __name__ == "__main__":
    pygame.init()
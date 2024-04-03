import pygame
import pygame.midi
from client.midi.play import get_midi_file_events
from client.utils.score import calc_score
import client.midi.play as play
import client.midi.voice_notes as voice_notes


# TODO [Aviral] Add KBD Support
class MidiGame:
    def __init__(
        self, midi_file_path, note_length, narrate_pitch=False, narrate_name=True
    ):
        self.midi_file = midi_file_path
        self.cur_events = []
        self.clock = pygame.time.Clock()
        self.note_length = note_length
        self.initialise_midi()
        self.initialise_narrator(narrate_pitch, narrate_name)

    def is_running(self):
        return self.midi_narrator.is_playing()

    def initialise_midi(self):
        pygame.midi.init()
        self.input_id = pygame.midi.get_default_input_id()
        if self.input_id == -1:
            print("No MIDI input devices found.")
            exit()

        self.midi_input = pygame.midi.Input(self.input_id)
        print(
            f"MIDI Input: {pygame.midi.get_device_info(self.input_id)[1].decode('ascii')}"
        )
        self.output_id = 0
        for i in range(pygame.midi.get_count()):
            if pygame.midi.get_device_info(i)[1] == b"Microsoft GS Wavetable Synth":
                self.output_id = i

        self.midi_output = pygame.midi.Output(self.output_id)
        print(
            f"MIDI Output: {pygame.midi.get_device_info(self.output_id)[1].decode('ascii')}"
        )

    def initialise_narrator(self, narrate_pitch, narrate_name):
        self.midi_narrator = play.MidiNarrator(
            self.midi_file,
            self.note_length,
            narrate_name,
            narrate_pitch,
            midi_out=self.midi_output,
        )

    def start(self):
        self.midi_narrator.play()

    def handle_events(self):
        if self.midi_input.poll():
            midi_events = self.midi_input.read(10)
            midi_evs = pygame.midi.midis2events(midi_events, self.midi_input.device_id)
            for event in midi_evs:
                if event.type == pygame.midi.MIDIIN:
                    note, velocity = event.data1, event.data2
                    note_on = True if event.status // 16 == 8 else False
                    note_off = True if event.status // 16 == 9 else False
                    if note_on:
                        print(voice_notes._midi_to_note(note), end=" ")
                        self.midi_output.note_on(note, velocity)
                        self.cur_events.append(["on", note, event.timestamp])
                    elif note_off:
                        self.midi_output.note_off(note)
                        self.cur_events.append(["off", note, event.timestamp])

    def stop(self):
        pygame.midi.quit()
        pygame.mixer.music.pause()
        self.midi_narrator.stop_playback()
        reference = get_midi_file_events(self.midi_file)
        return calc_score(self.cur_events, reference, self.note_length)


if __name__ == "__main__":
    pygame.init()
    game = MidiGame("assets/midi/happy_birthday.mid", 10, narrate_pitch=True)

    game.start()
    running = True
    while running:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                running = False
        game.handle_events()
        if not game.is_running():
            print(game.stop())
            running = False

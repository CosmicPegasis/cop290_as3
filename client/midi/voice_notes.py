import pygame.mixer
class VoiceNote:
    def __init__(self):
        self.d = {}
        notes = ['A', 'B', 'C', 'D','E','F', 'G']
        for i in range(9):
            for j in range(len(notes)):
                note_name = notes[j] + str(i)
                self.d[note_name] = pygame.mixer.Sound(f"assets/{note_name}.mp3")
    

    def _midi_to_note(self, midi_number):
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = (midi_number // 12) - 1
        note = note_names[midi_number % 12]
        return note + str(octave)

    def play_note(self, midi_number):
        self.d[self._midi_to_note(midi_number)].play()

    
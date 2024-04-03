import mido
import time
from client.midi.voice_notes import VoiceNote
import threading


def get_midi_file_events(midi_file):
    events = []
    cur_time = 0
    for msg in mido.MidiFile(midi_file):
        if not msg.is_meta:
            if msg.type == "note_on":
                events.append(["on", msg.note, cur_time * 1000])
                cur_time += msg.time
                events.append(["off", msg.note, cur_time * 1000])
    return events


class MidiNarrator(VoiceNote):
    def __init__(
        self, midi_file, slow, narrate_name=True, narrate_note=False, midi_out=None
    ):
        super().__init__()
        self.midi_events = []
        self.stop = False
        self.midi_file = midi_file
        self.slow = slow
        if narrate_note:
            self.midi_out = midi_out
        self.narrate_note = narrate_note
        self.narrate_name = narrate_name

    def _play(self):
        file = mido.MidiFile(self.midi_file)
        for msg in file:
            if not self.stop:
                if not msg.is_meta:
                    time.sleep(msg.time * self.slow)
                    if msg.type == "note_on" and msg.velocity > 0:
                        if self.narrate_name and self.narrate_note:
                            self.play_note(msg.note)
                            self.midi_out.note_on(msg.note, 100)
                        elif self.narrate_note:
                            self.midi_out.note_on(msg.note, 100)
                        else:
                            self.play_note(msg.note)
                    elif msg.type == "note_off":
                        self.midi_out.note_off(msg.note)

        time.sleep(0.5)

    def play(self):
        self.t = threading.Thread(target=self._play, daemon=True)
        self.t.start()

    def stop_playback(self):
        self.stop = True
        self.t.join()

    def is_playing(self):
        return self.t.is_alive()

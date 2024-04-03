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
    def __init__(self, midi_file, slow, midi_out=None):
        super().__init__()
        self.midi_events = []
        self.stop = False
        self.midi_file = midi_file
        self.slow = slow
        self.midi_out = midi_out
        # midi_out.note_on(60, 100)
        # time.sleep(5)
        # midi_out.note_off(60)

    def _play(self):
        file = mido.MidiFile(self.midi_file)
        for msg in file:
            if not self.stop:
                if self.midi_out:
                    time.sleep(msg.time * (self.slow / 2))
                else:
                    time.sleep(msg.time * self.slow)
                if not msg.is_meta:
                    if msg.type == "note_on":
                        if msg.velocity > 0:
                            # self.play_note(msg.note)
                            if self.midi_out:
                                self.midi_out.note_on(msg.note, 100)
                                time.sleep(msg.time * (self.slow / 2))
                                self.midi_out.note_off(msg.note)

        time.sleep(1)

    def play(self):
        self.t = threading.Thread(target=self._play, daemon=True)
        self.t.start()

    def stop_playback(self):
        self.stop = True
        self.t.join()

    def is_playing(self):
        return self.t.is_alive()

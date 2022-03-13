# Copyright 2022 Darren Elwood <darren@textnode.com> http://www.textnode.com @textnode

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at 
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Version 0.1

from pygame import midi

import util
import infinite_envelope as i_env
import sounds

class sound_factory():
    def __init__(self):
        self.tooling = sounds.pure_sine
        self.envelope = None
        self.envelope_freq = 0.0
        self.vibrato = None
        self.vibrato_freq = 0.0
        self.vibrato_depth = 0.0

    def retool(self, note):
        print("Retooling factory")
        if note == 40:
            self.tooling = sounds.pure_sine
        elif note == 41:
            self.tooling = sounds.pure_triangle
        elif note == 42:
            self.tooling = sounds.pure_sawtooth
        elif note == 43:
            self.tooling = sounds.pure_phased
        else:
            self.tooling = sounds.pure_sine
        print("Tooling is now: %s" % repr(self.tooling))

    def set_envelope_frequency(self, value):
        print("Setting envelope frequency")
        if value > 10:
            self.envelope = i_env.cosine
            self.envelope_freq = (value - 9.0) / 10.0
        else:
            self.envelope = None
            self.envelope_freq = 0.0
        print("Envelope frequency: %fHz" % self.envelope_freq)

    def set_vibrato_frequency(self, value):
        print("Setting vibrato frequency")
        if value > 10:
            self.vibrato_freq = (value - 9.0) / 10.0
        else:
            self.vibrato_freq = 0.0
        self.apply_vibrato_settings()
        print("Vibrato frequency: %fHz" % self.vibrato_freq)

    def set_vibrato_depth(self, value):
        print("Setting vibrato depth")
        if value > 10:
            self.vibrato_depth = (value - 9.0) / 10.0
        else:
            self.vibrato_depth = 0.0
        self.apply_vibrato_settings()
        print("Vibrato depth: %f" % self.vibrato_depth)

    def apply_vibrato_settings(self):
        if self.vibrato_depth > 0.0 and self.vibrato_freq > 0.0:
            self.vibrato = i_env.cosine
        else:
            self.vibrato = None

    def produce(self, note, velocity):
        if self.envelope != None and self.vibrato != None:
            return self.tooling(midi.midi_to_frequency(note), amplitude=util.amplitude_from_velocity(velocity), envelope=self.envelope(self.envelope_freq), freq_modulator=self.vibrato(self.vibrato_freq), freq_modulation_pct=self.vibrato_depth)
        elif self.envelope != None:
            return self.tooling(midi.midi_to_frequency(note), amplitude=util.amplitude_from_velocity(velocity), envelope=self.envelope(self.envelope_freq))
        elif self.vibrato != None:
            return self.tooling(midi.midi_to_frequency(note), amplitude=util.amplitude_from_velocity(velocity), freq_modulator=self.vibrato(self.vibrato_freq), freq_modulation_pct=self.vibrato_depth)
        else:
            return self.tooling(midi.midi_to_frequency(note), amplitude=util.amplitude_from_velocity(velocity))

# Copyright 2022 Darren Elwood <darren@textnode.com> http://www.textnode.com @textnode
#
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
        self.envelope = i_env.flat
        self.envelope_freq = 0.0

    def retool(self, note):
        print("Retooling factory")
        if note == 40:
            self.tooling = sounds.pure_sine
        elif note == 41:
            self.tooling = sounds.pure_square
        elif note == 42:
            self.tooling = sounds.pure_triangle
        elif note == 43:
            self.tooling = sounds.pure_sawtooth
        elif note == 36:
            self.tooling = sounds.pure_phased
        elif note == 37:
            self.tooling = sounds.pure_square
        elif note == 38:
            self.tooling = sounds.pure_triangle
        elif note == 39:
            self.tooling = sounds.pure_sawtooth
        else:
            self.tooling = sounds.pure_sine

    def remodulate(self, value):
        print("Remodulating factory")
        if value > 10:
            self.envelope = i_env.cosine
            self.envelope_freq = (value - 9.0) / 30.0
        else:
            self.envelope = i_env.flat
            self.envelope_freq = 0.0
        print("Envelope frequency: %fHz" % self.envelope_freq)

    def produce(self, note, velocity):
        return self.tooling(midi.midi_to_frequency(note), amplitude=util.amplitude_from_velocity(velocity), envelope=self.envelope(self.envelope_freq))

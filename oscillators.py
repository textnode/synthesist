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

from abc import ABC, abstractmethod
from collections.abc import Generator
import math

import shared

class oscillator(Generator):

    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__()
        print("Oscillator with base frequency: %fHz" % base_freq)
        self.base_freq = base_freq
        self.current_freq = self.base_freq
        self.current_phase = start_phase
        self.end_phase = end_phase
        self.freq_modulator = freq_modulator
        self.freq_modulation_pct = freq_modulation_pct
        self.gap = (math.pi * 2 * self.base_freq) / shared.sample_rate

    def exhausted(self):
        if self.end_phase != None:
            if self.current_phase > self.end_phase:
                raise StopIteration

    def modulate(self):
        if self.freq_modulator != None:
            self.current_freq = self.base_freq + (self.base_freq * self.freq_modulation_pct / 100.0 * next(self.freq_modulator))
            self.gap = (math.pi * 2 * self.current_freq) / shared.sample_rate

    @abstractmethod
    def send(self, ignored_arg):
        pass

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration


class sine(oscillator):
    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__(base_freq, start_phase, end_phase, freq_modulator, freq_modulation_pct)

    def send(self, ignored_arg):
        super().exhausted()
        self.modulate()
        val = math.sin(float(self.current_phase))
        self.current_phase = self.current_phase + self.gap
        return val

class cosine(oscillator):
    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__(base_freq, start_phase, end_phase, freq_modulator, freq_modulation_pct)

    def send(self, ignored_arg):
        super().exhausted()
        self.modulate()
        val = math.cos(float(self.current_phase))
        self.current_phase = self.current_phase + self.gap
        return val

class square(oscillator):
    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__(base_freq, start_phase, end_phase, freq_modulator, freq_modulation_pct)

    def send(self, ignored_arg):
        super().exhausted()
        self.modulate()
        val = 1.0 if self.current_phase % (math.pi * 2) < math.pi else -1.0
        self.current_phase = self.current_phase + self.gap
        return val

class triangle(oscillator):
    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__(base_freq, start_phase, end_phase, freq_modulator, freq_modulation_pct)

    def send(self, ignored_arg):
        super().exhausted()
        self.modulate()
        ph = self.current_phase % (2 * math.pi)
        if ph < math.pi:
            val = ((ph / math.pi) * 2) - 1
        else:
            val = ((((2 * math.pi) - ph) / math.pi) * 2) - 1
        self.current_phase = self.current_phase + self.gap
        return val

class sawtooth(oscillator):
    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__(base_freq, start_phase, end_phase, freq_modulator, freq_modulation_pct)

    def send(self, ignored_arg):
        super().exhausted()
        self.modulate()
        ph = self.current_phase % (2 * math.pi)
        val = (ph / math.pi) - 1
        self.current_phase = self.current_phase + self.gap
        return val

class reverse_sawtooth(oscillator):
    def __init__(self, base_freq, start_phase=0.0, end_phase=None, freq_modulator=None, freq_modulation_pct=0.0):
        super().__init__(base_freq, start_phase, end_phase, freq_modulator, freq_modulation_pct)

    def send(self, ignored_arg):
        super().exhausted()
        self.modulate()
        ph = self.current_phase % (2 * math.pi)
        val = (((2 * math.pi) - ph) / math.pi) - 1
        self.current_phase = self.current_phase + self.gap
        return val

class constant(Generator):
    def __init__(self, duration=None, amplitude=1.0):
        super().__init__()
        self.samples = None
        if duration != None:
            self.samples = int(duration * shared.sample_rate)
        self.amplitude = amplitude

    def send(self, ignored_arg):
        if(self.samples != None):
            if(self.samples > 0):
                self.samples -= 1
                #print("%s Samples remaining: %d" % (repr(self), self.samples))
            else:
                raise StopIteration
        return self.amplitude

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class silence(constant):
    def __init__(self, duration):
        super().__init__(duration=duration, amplitude=0.0)


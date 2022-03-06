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

from collections.abc import Generator

import shared

class phaser(Generator):
    def __init__(self, inp, input_to_be_delayed, initial_delay, control):
        self.inp = inp
        self.input_to_be_delayed = input_to_be_delayed
        self.shift = initial_delay
        self.control = control
        self.current_delay = 0

    def send(self, ignored_arg):
        self.shift += int(next(self.control) * 10)

        while self.shift > 0:
            next(self.inp)
            self.shift -= 1
            self.current_delay += 1
        while self.shift < 0:
            next(self.input_to_be_delayed)
            self.shift += 1
            self.current_delay += 1

        return (next(self.inp) + next(self.input_to_be_delayed)) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration


class echoer(Generator):
    def __init__(self, striker, delay, decay, repeats):
        self.striker = striker
        self.delay = int(delay * shared.sample_rate)
        self.decay = decay
        self.repeats = repeats
        self.source = []
        self.replay = []
        self.amplitude = 1.0
        self.replay_index = None
        
    def send(self, ignored_arg):
        try:
            self.source.append(next(self.striker))
            return self.source[-1]
        except StopIteration:
            pass
        if len(self.replay) == 0:
            for _ in range(self.repeats):
                for _ in range(self.delay - len(self.source)):
                    self.replay.append(0.0)
                self.amplitude = self.amplitude * self.decay
                for element in self.source:
                    self.replay.append(element * self.amplitude)
            self.replay_index = 0
        if(self.replay_index < len(self.replay)):
            val = self.replay[self.replay_index]
            self.replay_index += 1
            return val
        else:
            raise StopIteration

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def release(self):
        pass



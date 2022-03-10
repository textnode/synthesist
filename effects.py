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
import itertools

import shared
import util
import oscillators as osc

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

class echo(Generator):
    def __init__(self, generator, delay, decay, repeats):
        current_delay = 0
        current_amplitude = 1.0
        copies = itertools.tee(generator, repeats+1)
        self.generators = []
        self.exhausted_generators = []
        for copy in copies:
            #print("Adding copy with delay: %f and amplitude: %f" % (current_delay, current_amplitude))
            self.generators.append(itertools.chain(osc.silence(current_delay), util.scaler(copy, current_amplitude)))
            current_delay += delay
            current_amplitude *= decay

    def send(self, ignored_arg):
        sig = 0.0
        if len(self.generators) == len(self.exhausted_generators):
            raise StopIteration
        for generator in self.generators:
            if generator not in self.exhausted_generators:
                try:
                  sig += next(generator)
                except StopIteration:
                  self.exhausted_generators.append(generator)
                  #print("Generator %s exhausted" % repr(generator))
        sig /= len(self.generators)
        return sig

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def release(self):
        pass


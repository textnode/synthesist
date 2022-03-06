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
import random

import shared

class stepper(Generator):

    def __init__(self, step_size=10, base_amplitude=1.0, envelope=None, envelope_pct=0.0):
        self.position = 0
        self.step_size = step_size
        self.base_amplitude = base_amplitude
        self.envelope = envelope
        self.envelope_pct = envelope_pct
        self.amplitude = self.base_amplitude

    def modulate(self):
        #print("modulate noise")
        if self.envelope != None:
            #print("has envelope")
            try:
                self.amplitude = self.base_amplitude * ((self.base_amplitude * self.envelope_pct / 100.0) * ((next(self.envelope))))
            except StopIteration:
                #print("stop iteration")
                raise

    @abstractmethod
    def send(self, ignored_arg):
        pass

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration


class uniform_rand(stepper):
    random.seed(shared.seed)
    uniform_rands = []
    for _ in range(shared.sample_rate):
        rand = random.uniform(-1.0, 1.0)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)
        uniform_rands.append(rand)

    def send(self, ignored_arg):
        self.modulate()
        val = uniform_rand.uniform_rands[self.position % len(uniform_rand.uniform_rands)] * self.amplitude
        self.position += self.step_size
        return val



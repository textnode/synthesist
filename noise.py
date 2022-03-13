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

    def __init__(self, step_size=10, base_amplitude=1.0):
        super().__init__()
        self.position = 0
        self.step_size = step_size
        self.base_amplitude = base_amplitude
        self.amplitude = self.base_amplitude

    @abstractmethod
    def send(self, ignored_arg):
        pass

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration


class uniform_rand(stepper):
    def __init__(self, step_size=10, base_amplitude=1.0):
        super().__init__(step_size, base_amplitude)

        random.seed(shared.seed)
        self.uniform_rands = []
        for _ in range(shared.sample_rate):
            rand = random.uniform(-1.0, 1.0)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)
            self.uniform_rands.append(rand)

    def send(self, ignored_arg):
        val = self.uniform_rands[self.position % len(self.uniform_rands)] * self.amplitude
        self.position += self.step_size
        return val



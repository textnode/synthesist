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
import math
import itertools

import oscillators as osc

class sine(Generator):
    def __init__(self, freq, start_phase=0.0):
        super().__init__()
        self.gen = itertools.cycle(osc.sine(freq, start_phase=start_phase, end_phase=math.pi * 2))

    def send(self, ignored_arg):
        return (next(self.gen) + 1.0) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class cosine(Generator):
    def __init__(self, freq, start_phase=0.0):
        super().__init__()
        self.gen = itertools.cycle(osc.cosine(freq, start_phase=start_phase, end_phase=math.pi * 2))

    def send(self, ignored_arg):
        return (next(self.gen) + 1.0) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class square(Generator):
    def __init__(self, freq, start_phase=0.0):
        super().__init__()
        self.gen = itertools.cycle(osc.square(freq, start_phase=start_phase, end_phase=math.pi * 2))

    def send(self, ignored_arg):
        return (next(self.gen) + 1.0) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class triangle(Generator):
    def __init__(self, freq, start_phase=0.0):
        super().__init__()
        self.gen = itertools.cycle(osc.triangle(freq, start_phase=start_phase, end_phase=math.pi * 2))

    def send(self, ignored_arg):
        return (next(self.gen) + 1.0) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class sawtooth(Generator):
    def __init__(self, freq, start_phase=0.0):
        super().__init__()
        self.gen = itertools.cycle(osc.sawtooth(freq, start_phase=start_phase, end_phase=math.pi * 2))

    def send(self, ignored_arg):
        return (next(self.gen) + 1.0) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class reverse_sawtooth(Generator):
    def __init__(self, freq, start_phase=0.0):
        super().__init__()
        self.gen = itertools.cycle(osc.reverse_sawtooth(freq, start_phase=start_phase, end_phase=math.pi * 2))

    def send(self, ignored_arg):
        return (next(self.gen) + 1.0) / 2.0

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration


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

import itertools
from collections.abc import Generator
import math

import shared

def __constant(value, duration=None):
    if duration != None:
        return itertools.repeat(value, int(duration * shared.sample_rate))
    else:
        return itertools.repeat(value)

def max(duration=None):
    return __constant(1.0, duration)

def silence(duration=None):
    return __constant(0.0, duration)

def amplitude_from_velocity(velocity):
    return (1.0/127) * velocity

class combine2(Generator):
    #returns mean of 2 input values
    def __init__(self, gen1, gen2):
        super().__init__()
        self.gen1 = gen1
        self.gen2 = gen2

    def send(self, ignored_arg):
        return((next(self.gen1) + next(self.gen2)) / 2.0)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class combine3(Generator):
    #returns mean of 3 input values
    def __init__(self, gen1, gen2, gen3):
        super().__init__()
        self.gen1 = gen1
        self.gen2 = gen2
        self.gen3 = gen3

    def send(self, ignored_arg):
        return((next(self.gen1) + next(self.gen2) + next(self.gen3)) / 3.0)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class minZeroer(Generator):
    #output never goes below zero
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def send(self, ignored_arg):
        return(max(0.0, next(self.gen)))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class fabser(Generator):
    #outputs under zero are reflected to positive values
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def send(self, ignored_arg):
        return(math.fabs(next(self.gen)))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class inverter(Generator):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def send(self, ignored_arg):
        return(-1.0 * next(self.gen))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class scaler(Generator):
    def __init__(self, gen, scaling_factor):
        super().__init__()
        self.gen = gen
        self.scaling_factor = scaling_factor

    def send(self, ignored_arg):
        return(next(self.gen) * self.scaling_factor)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class multiplier(Generator):
    def __init__(self, gen1, gen2):
        super().__init__()
        self.gen1 = gen1
        self.gen2 = gen2

    def send(self, ignored_arg):
        return(next(self.gen1) * next(self.gen2))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class offsetter(Generator):
    def __init__(self, gen, offset):
        super().__init__()
        self.gen = gen
        self.offset = offset

    def send(self, ignored_arg):
        return(next(self.gen) + self.offset)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class limiter(Generator):
    def __init__(self, gen, upper_limit=1.0, lower_limit=-1.0):
        super().__init__()
        self.gen = gen
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

    def send(self, ignored_arg):
        return min(max(next(self.gen), self.lower_limit), self.upper_limit)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class truncater(Generator):
    def __init__(self, gen, max_duration):
        super().__init__()
        self.gen = gen
        self.samples = shared.sample_rate * max_duration

    def send(self, ignored_arg):
        self.samples -= 1
        if self.samples < 0:
            raise StopIteration
        return next(self.gen)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

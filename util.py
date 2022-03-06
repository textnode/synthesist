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


class adder(Generator):
    #returns mean of 2 input values
    def __init__(self, gen1, gen2):
        self.gen1 = gen1
        self.gen2 = gen2

    def send(self, ignored_arg):
        return((next(self.gen1) + next(self.gen2)) / 2.0)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class minZeroer(Generator):
    #output never goes below zero
    def __init__(self, gen1):
        self.gen1 = gen1

    def send(self, ignored_arg):
        return(max(0.0, next(self.gen1)))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class fabser(Generator):
    #outputs under zero are reflected to positive values
    def __init__(self, gen1):
        self.gen1 = gen1

    def send(self, ignored_arg):
        return(math.fabs(next(self.gen1)))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class inverter(Generator):
    def __init__(self, gen1):
        self.gen1 = gen1

    def send(self, ignored_arg):
        return(-1.0 * next(self.gen1))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class scaler(Generator):
    def __init__(self, gen1, factor):
        self.gen1 = gen1
        self.factor = factor

    def send(self, ignored_arg):
        return(next(self.gen1) * self.factor)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

class multiplier(Generator):
    def __init__(self, gen1, gen2):
        self.gen1 = gen1
        self.gen2 = gen2

    def send(self, ignored_arg):
        return(next(self.gen1) * next(self.gen2))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration


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


class presser(Generator):
    def __init__(self, gen, attack_gen, decay_gen, sustain_gen, release_gen):
        super().__init__()
        self.gen = gen
        self.attack_gen = attack_gen
        self.last_attack = 1.0
        self.decay_gen = decay_gen
        self.last_decay = 1.0
        self.sustain_gen = sustain_gen
        self.last_sustain = 1.0
        self.release_gen = release_gen
        self.released = False

    def send(self, ignored_arg):
        try:
            self.last_attack = next(self.attack_gen)
            #print("Attack phase")
            return self.last_attack * next(self.gen)
        except StopIteration:
            pass

        try:
            self.last_decay = next(self.decay_gen)
            #print("Decay phase")
            return self.last_attack * self.last_decay * next(self.gen)
        except StopIteration:
            pass

        if not self.released:
            self.last_sustain = next(self.sustain_gen)
            #print("Sustain phase")
            return self.last_attack * self.last_decay * self.last_sustain * next(self.gen)

        #print("Release phase")
        return self.last_attack * self.last_decay * self.last_sustain * next(self.release_gen) * next(self.gen)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def release(self):
        self.released = True


class striker(Generator):
    def __init__(self, gen, attack_gen, decay_gen, release_gen):
        super().__init__()
        self.gen = gen
        self.attack_gen = attack_gen
        self.decay_gen = decay_gen
        self.release_gen = release_gen
        self.released = False

    def send(self, ignored_arg):
        try:
            self.last_attack = next(self.attack_gen)
            return self.last_attack * next(self.gen)
        except StopIteration:
            pass

        try:
            self.last_decay = next(self.decay_gen)
            return self.last_attack * self.last_decay * next(self.gen)
        except StopIteration:
            pass

        return self.last_attack * self.last_decay * next(self.release_gen) * next(self.gen)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def release(self):
        pass



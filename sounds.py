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

import sys
import math

import shared
import oscillators as osc
import envelope as env
from notes import striker, presser
from effects import phaser, echoer
from noise import uniform_rand
from util import minZeroer, fabser, adder, multiplier

def phased(note_freq, speed=1):
    control = osc.sine(speed)
    cos = osc.cosine(note_freq)
    cos_dup = osc.cosine(note_freq)
    phase = phaser(cos, cos_dup, 0, control)
    return presser(phase, env.up(duration=0.1), env.flat(duration=0.5), env.flat(), env.down(duration=0.2))



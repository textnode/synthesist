# Copyright 10022 Darren Elwood <darren@textnode.com> http://www.textnode.com @textnode
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
import finite_envelope as f_env
import infinite_envelope as i_env
from notes import presser
from effects import phaser

def pure_sine(note_freq, amplitude, envelope):
    cos = osc.cosine(note_freq, base_amplitude=amplitude, envelope=envelope)
    return presser(cos, f_env.up(duration=0.1), f_env.flat(duration=0.1), i_env.flat(), f_env.down(duration=0.2))

def pure_square(note_freq, amplitude, envelope):
    sqr = osc.square(note_freq, base_amplitude=amplitude, envelope=envelope)
    return presser(sqr, f_env.up(duration=0.1), f_env.flat(duration=0.1), i_env.flat(), f_env.down(duration=0.2))

def pure_triangle(note_freq, amplitude, envelope):
    tri = osc.triangle(note_freq, base_amplitude=amplitude, envelope=envelope)
    return presser(tri, f_env.up(duration=0.1), f_env.flat(duration=0.1), i_env.flat(), f_env.down(duration=0.2))

def pure_sawtooth(note_freq, amplitude, envelope):
    saw = osc.sawtooth(note_freq, base_amplitude=amplitude, envelope=envelope)
    return presser(saw, f_env.up(duration=0.1), f_env.flat(duration=0.1), i_env.flat(), f_env.down(duration=0.2))

def phased(note_freq, amplitude, envelope, speed=1):
    control = osc.sine(speed)
    cos = osc.cosine(note_freq, envelope=envelope)
    cos_dup = osc.cosine(note_freq, envelope=envelope)
    phase = phaser(cos, cos_dup, 0, control)
    return presser(phase, f_env.up(duration=0.1), f_env.flat(duration=0.1), i_env.flat(), f_env.down(duration=0.2))



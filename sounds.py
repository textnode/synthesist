# Copyright 20.2 Darren Elwood <darren@textnode.com> http://www.textnode.com @textnode
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
# Version 0.2

import sys
import math
import itertools

import shared
import oscillators as osc
import finite_envelope as f_env
import infinite_envelope as i_env
from notes import presser, striker
from effects import phaser
import noise
import util

def pure_sine(note_freq, amplitude=1.0, envelope=util.max()):
    cos = itertools.cycle(osc.cosine(note_freq))
    return presser(util.scaler(cos, scaling_factor=amplitude), f_env.up(duration=0.2), util.max(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_square(note_freq, amplitude=1.0, envelope=util.max()):
    sqr = itertools.cycle(osc.square(note_freq))
    return presser(util.scaler(sqr, scaling_factor=amplitude), f_env.up(duration=0.2), util.max(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_triangle(note_freq, amplitude=1.0, envelope=util.max()):
    tri = itertools.cycle(osc.triangle(note_freq))
    return presser(util.scaler(tri, scaling_factor=amplitude), f_env.up(duration=0.2), util.max(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_sawtooth(note_freq, amplitude=1.0, envelope=util.max()):
    saw = itertools.cycle(osc.sawtooth(note_freq))
    return presser(util.scaler(saw, scaling_factor=amplitude), f_env.up(duration=0.2), util.max(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_phased(note_freq, amplitude=1.0, envelope=util.max(), speed=1.0):
    control = itertools.cycle(osc.sine(speed))
    cos = itertools.cycle(osc.cosine(note_freq))
    cos_dup = itertools.cycle(osc.cosine(note_freq))
    phase = phaser(cos, cos_dup, 0, control)
    return presser(util.scaler(phase, scaling_factor=amplitude), f_env.up(duration=0.2), util.max(duration=0.2), envelope, f_env.down(duration=1.0))

def cymbal(amplitude=0.05, envelope=util.max()):
    noi1 = itertools.cycle(noise.uniform_rand(step_size=5))
    noi2 = itertools.cycle(noise.uniform_rand(step_size=10))
    comb = util.combine2(noi1, noi2)
    return presser(util.scaler(comb, scaling_factor=amplitude), f_env.up(duration=0.05), util.max(duration=0.2), envelope, f_env.down(duration=1.0))

def snare(amplitude=0.05):
    noi3 = itertools.cycle(noise.uniform_rand(step_size=10))
    strike = striker(util.scaler(noi3, scaling_factor=amplitude), f_env.up(duration=0.01), util.max(duration=0.12), f_env.down(duration=0.01))
    return strike

def bass(amplitude=1.0):
    sin1 = itertools.cycle(osc.sine(200))
    sin2 = itertools.cycle(osc.sine(300))
    sin3 = itertools.cycle(osc.sine(400))
    comb = util.combine3(sin1, sin2, sin3)
    strike = striker(util.scaler(comb, scaling_factor=amplitude), f_env.up(duration=0.01), util.max(duration=0.02), f_env.down(duration=0.12))
    return strike


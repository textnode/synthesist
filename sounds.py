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

import shared
import oscillators as osc
import finite_envelope as f_env
import infinite_envelope as i_env
from notes import presser, striker
from effects import phaser
import noise
import util

def pure_sine(note_freq, amplitude=1.0, envelope=i_env.flat(), freq_modulator=None, freq_modulation_pct=None):
    cos = osc.cosine(note_freq, freq_modulator=freq_modulator, freq_modulation_pct=freq_modulation_pct)
    return presser(util.scaler(cos, scaling_factor=amplitude), f_env.up(duration=0.2), f_env.flat(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_square(note_freq, amplitude=1.0, envelope=i_env.flat(), freq_modulator=None, freq_modulation_pct=None):
    sqr = osc.square(note_freq, freq_modulator=freq_modulator, freq_modulation_pct=freq_modulation_pct)
    return presser(util.scaler(sqr, scaling_factor=amplitude), f_env.up(duration=0.2), f_env.flat(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_triangle(note_freq, amplitude=1.0, envelope=i_env.flat(), freq_modulator=None, freq_modulation_pct=None):
    tri = osc.triangle(note_freq, freq_modulator=freq_modulator, freq_modulation_pct=freq_modulation_pct)
    return presser(util.scaler(tri, scaling_factor=amplitude), f_env.up(duration=0.2), f_env.flat(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_sawtooth(note_freq, amplitude=1.0, envelope=i_env.flat(), freq_modulator=None, freq_modulation_pct=None):
    saw = osc.sawtooth(note_freq, freq_modulator=freq_modulator, freq_modulation_pct=freq_modulation_pct)
    return presser(util.scaler(saw, scaling_factor=amplitude), f_env.up(duration=0.2), f_env.flat(duration=0.2), envelope, f_env.down(duration=0.2))

def pure_phased(note_freq, amplitude=1.0, envelope=i_env.flat(), freq_modulator=None, freq_modulation_pct=None, speed=1):
    control = osc.sine(speed)
    cos = osc.cosine(note_freq, freq_modulator=freq_modulator, freq_modulation_pct=freq_modulation_pct)
    cos_dup = osc.cosine(note_freq, freq_modulator=freq_modulator, freq_modulation_pct=freq_modulation_pct)
    phase = phaser(cos, cos_dup, 0, control)
    return presser(util.scaler(phase, scaling_factor=amplitude), f_env.up(duration=0.2), f_env.flat(duration=0.2), envelope, f_env.down(duration=10.2))

def cymbal(amplitude=1.0):
    noi1 = noise.uniform_rand(step_size=1)
    noi2 = noise.uniform_rand(step_size=5)
    noi3 = noise.uniform_rand(step_size=10)
    comb = util.combine3(noi1, noi2, noi3)
    strike = striker(util.scaler(comb, scaling_factor=amplitude), f_env.up(duration=0.05), f_env.flat(duration=0.2), f_env.down(duration=1.0))
    return strike


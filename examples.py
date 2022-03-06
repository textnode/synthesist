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
from notes import striker
from effects import phaser, echoer
from noise import uniform_rand
from util import minZeroer, fabser, adder, multiplier

#testing some combinations of oscillators, envelopes, echo and phasing

control = osc.cosine(1, start_phase=math.pi / 2)
cos = osc.cosine(200, start_phase = math.pi / 2)
cos_dup = osc.cosine(200, start_phase = math.pi / 2)
phase = phaser(cos, cos_dup, 0, control)
strike = striker(phase, env.up(0.5), env.flat(1, 0.5), env.down(0.5))
echo = echoer(strike, 1.5, 0.8, 3)
shared.play(echo)

sig_env = env.sine(4, duration=1.0)
min_env = fabser(sig_env)
sig = osc.cosine(441, envelope=min_env, envelope_pct=5.0)
noise_env = env.cosine(2, duration=1.0)
noise = uniform_rand(step_size=1, base_amplitude=1.0, envelope=noise_env, envelope_pct=5.0)
add = adder(sig, noise)
strike = striker(add, env.up(1.0), env.down_30_pct(1.0), env.down(1.0))
shared.play(strike)

strike = striker(osc.cosine(4410), env.up(duration=0.1), env.down_30_pct(duration=0.1), env.down(duration=2.0))
shared.play(strike)


shared.play(striker(osc.cosine(441), env.up(0.1), env.down_30_pct(0.1), env.down(0.1)))
shared.play(striker(osc.cosine(882), env.up(0.1), env.down_30_pct(0.1), env.down(0.1)))
shared.play(striker(osc.cosine(1764), env.up(0.1), env.down_30_pct(0.1), env.down(0.1)))


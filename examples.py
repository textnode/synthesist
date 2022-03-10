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
from effects import phaser, echo
from noise import uniform_rand
from util import minZeroer, fabser, combiner, multiplier, offsetter, scaler

#testing some combinations of oscillators, envelopes, echo and phasing

#control = osc.cosine(1, start_phase=math.pi / 2)
#scaled = scaler(control, scaling_factor=0.3)
#offset = offsetter(scaled, offset=1.0)
#shared.plot(offset)
#sys.exit(0)



cos = osc.cosine(441, end_phase=math.pi*2*441)
shared.play(cos)

strike = striker(osc.cosine(4410), env.up(duration=0.1), env.down_30_pct(duration=0.1), env.down(duration=2.0))
shared.play(strike)

control = osc.cosine(1, start_phase=math.pi / 2)
cos = osc.cosine(441, start_phase = math.pi / 2)
cos_dup = osc.cosine(441, start_phase = math.pi / 2)
phase = phaser(cos, cos_dup, 0, control)
shared.play(phase, max_duration=2)

control = osc.cosine(1, start_phase=math.pi / 2)
cos = osc.cosine(441, start_phase = math.pi / 2)
cos_dup = osc.cosine(441, start_phase = math.pi / 2)
phase = phaser(cos, cos_dup, 0, control)
strike = striker(phase, env.up(duration=0.201), env.flat(duration=0.401), env.down(duration=0.201))
echo = echo(strike, 0.9, 0.8, 5)
shared.play(echo)

sig_env = env.sine(4, duration=10.0)
min_env = fabser(sig_env)
sig = osc.cosine(441, envelope=min_env, envelope_pct=5.0)
noise_env = env.cosine(2, duration=10.0)
noise = uniform_rand(step_size=1, base_amplitude=1.0, envelope=noise_env, envelope_pct=5.0)
add = combiner(sig, noise)
strike = striker(add, env.up(3.0), env.down_30_pct(5.0), env.down(2.0))
shared.play(strike)

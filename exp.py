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
import noise

import infinite_envelope as i_env
import finite_envelope as f_env

import util
import notes
import effects
import sounds

noise_env = i_env.reverse_sawtooth(8)
offs_env = util.offsetter(noise_env, 0.7)
lim_env = util.limiter(offs_env, upper_limit=1.0, lower_limit=0.5)
trunc_env = util.truncater(lim_env, 2.0)

noi1 = noise.uniform_rand(step_size=1)
noi2 = noise.uniform_rand(step_size=5)
noi3 = noise.uniform_rand(step_size=10)

comb = util.combine3(noi1, noi2, noi3)

strike = notes.striker(comb, f_env.up(0.01), trunc_env, f_env.down(2.0))
shared.play(strike, max_duration=10.0)



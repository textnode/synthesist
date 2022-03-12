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

#play a few sounds
control = osc.cosine(1, start_phase=math.pi / 2)
cos = osc.cosine(441, start_phase = math.pi / 2)
cos_dup = osc.cosine(441, start_phase = math.pi / 2)
phase = effects.phaser(cos, cos_dup, 0, control)
strike = notes.striker(phase, f_env.up(0.100), f_env.flat(0.300), f_env.down(0.100))
echo = effects.echo(strike, 1.0, 0.5, 3)
shared.play(echo)

sig_env = i_env.sine(4)
min_env = util.fabser(sig_env)
sig = osc.cosine(441, envelope=min_env)
noise_env = i_env.cosine(2)
noise = noise.uniform_rand(step_size=1, envelope=noise_env)
add = util.combiner(sig, noise)
strike = notes.striker(add, f_env.up(3.0), f_env.down_30_pct(5.0), f_env.down(2.0))
shared.play(strike)



#plot the output of each class to eyeball for correctness
shared.plot(osc.sine(441, end_phase=31.4), title="Sine 441Hz ~ 10 cycles")

shared.plot(osc.cosine(441, end_phase=31.4), title="Cosine 441Hz ~ 10 cycles")
shared.plot(osc.square(441, end_phase=31.4), title="Square 441Hz ~ 10 cycles")
shared.plot(osc.triangle(441, end_phase=31.4), title="Triangle 441Hz ~ 10 cycles")
shared.plot(osc.sawtooth(441, end_phase=31.4), title="Sawtooth 441Hz ~ 10 cycles")
shared.plot(osc.reverse_sawtooth(441, end_phase=31.4), title="Reverse sawtooth 441Hz ~ 10 cycles")
shared.plot(osc.constant(duration=0.1), title="Constant 1.0 for 0.1 seconds")
shared.plot(osc.silence(duration=0.1), title="Silence for 0.1 seconds")

shared.plot(f_env.up(duration=1.0), title="Finite up envelope taking 1 second")
shared.plot(f_env.down(duration=1.0), title="Finite down envelope taking 1 second")
shared.plot(f_env.down_30_pct(duration=1.0), title="Finite down 30% envelope taking 1 second")
shared.plot(f_env.flat(1.0), title="Finite flat 1.0 envelope taking 1 second")

shared.plot(i_env.sine(441), max_duration=0.01, title="Infinite sine 441Hz envelope, terminated at 0.01 seconds")
shared.plot(i_env.cosine(441), max_duration=0.01, title="Infinite cosine 441Hz envelope, terminated at 0.01 seconds")
shared.plot(i_env.square(441), max_duration=0.01, title="Infinite square 441Hz envelope, terminated at 0.01 seconds")
shared.plot(i_env.triangle(441), max_duration=0.01, title="Infinite triangle 441Hz envelope, terminated at 0.01 seconds")
shared.plot(i_env.sawtooth(441), max_duration=0.01, title="Infinite sawtooth 441Hz envelope, terminated at 0.01 seconds")
shared.plot(i_env.reverse_sawtooth(441), max_duration=0.01, title="Infinite reverse-sawtooth 441Hz envelope, terminated at 0.01 seconds")
shared.plot(i_env.flat(1.0), max_duration=0.01, title="Infinite flat 1.0 envelope, terminated at 0.01 seconds")

#shared.plot(noise.uniform_rand(step_size=1), max_duration=0.01, title="Infinite random noise, terminated at 0.01 seconds")

#notes.presser()
shared.plot(notes.striker(osc.sine(441), f_env.up(1.0), f_env.flat(1.0), f_env.down(1.0)), title="Striker note, 441Hz Sine with envelopes: up 1 second, flat 1 second, down 1 second")

shared.plot(util.combiner(osc.sine(441), osc.square(220)), max_duration=0.01, title="Sine 441Hz and square 220Hz combined, terminated at 0.01 seconds")
shared.plot(util.minZeroer(osc.sine(441)), max_duration=0.01, title="Sine 441Hz min-zeroed, terminated at 0.01 seconds")
shared.plot(util.fabser(osc.sine(441)), max_duration=0.01, title="Sine 441Hz fabsd, terminated at 0.01 seconds")
shared.plot(util.inverter(osc.sine(441)), max_duration=0.01, title="Sine 441Hz inverted, terminated at 0.01 seconds")
shared.plot(util.scaler(osc.sine(441), scaling_factor=2.0), max_duration=0.01, title="Sine 441Hz scale by factor of 2.0, terminated at 0.01 seconds")
shared.plot(util.multiplier(osc.sine(441), osc.square(220)), max_duration=0.01, title="Sine 441Hz multiplied by square 220Hz, terminated at 0.01 seconds")
shared.plot(util.offsetter(osc.sine(441), offset=1.0), max_duration=0.01, title="Sine 441Hz offset by 1.0, terminated at 0.01 seconds")
shared.plot(util.limiter(osc.sine(441, base_amplitude=2.0), upper_limit=1.5, lower_limit=-0.7), max_duration=0.01, title="Sine 441Hz with amplitude 2.0 limited to upper limit 1.5 and lower limit -0.7, terminated at 0.01 seconds")




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

import itertools
import random

import shared

random.seed(shared.seed)
uniform_rands = []
for _ in range(shared.sample_rate):
    rand = random.uniform(-1.0, 1.0)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)
    uniform_rands.append(rand)

def uniform_rand(step_size=10):
    return itertools.cycle(itertools.islice(uniform_rands, 0, None, step_size))



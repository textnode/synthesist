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
import math

import oscillators as osc
import shared

class cycle_cache():
    def __init__(self):
        self.cache = {}
        for frequency in range(1, 2000000, 1):
            self.cache[frequency / 100.0] = list(osc.square(frequency / 100.0, end_phase=math.pi / 2))
   

cyc = cycle_cache() 

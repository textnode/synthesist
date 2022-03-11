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

import math

from oscillators import sine, cosine, constant

class up(sine):
    def __init__(self, duration):
        start = 0.0
        end = math.pi / 2
        freq = ((end - start) / (2 * math.pi)) / duration
        super().__init__(freq, start_phase=start, end_phase=end)

class down(cosine):
    def __init__(self, duration):
        start = 0.0
        end = math.pi / 2
        freq = ((end - start) / (2 * math.pi)) / duration
        super().__init__(freq, start_phase=start, end_phase=end)

class down_30_pct(cosine):
    def __init__(self, duration):
        start = 0.0
        end = math.pi / 4
        freq = ((end - start) / (2 * math.pi)) / duration
        super().__init__(freq, start_phase=start, end_phase=end)

class flat(constant):
    def __init__(self, duration, amplitude=1.0):
        super().__init__(duration, amplitude)


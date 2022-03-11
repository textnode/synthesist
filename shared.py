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

from array import array
import struct
import math
import itertools

import pyaudio
from matplotlib import pyplot as plt

sample_rate = 22050
scaling = 32500.0
frames_per_buffer = 1024
seed = math.pi

def plot(gen, max_duration=sample_rate * 10, title=None):
    # max_duration is here to save me from the easy mistake of passing in an infinite generator.
    audio = []
    for sig in itertools.islice(gen, 0, int(max_duration * sample_rate)):
        audio.append(sig)
    plt.plot(audio)
    if title != None:
        plt.title(title)
    plt.show()


def play(gen, max_duration=sample_rate * 10):
    # max_duration is here to save me from the easy mistake of passing in an infinite generator.
    audio = array('i')
    for samp in itertools.islice(gen, 0, int(max_duration * sample_rate)):
        #print("sig: %f" % samp)
        audio.append(int( (samp) * scaling))
    packed = struct.pack("<%si" % len(audio), *audio)
    audio = pyaudio.PyAudio()
    stream = audio.open(rate=sample_rate, channels=1, format=pyaudio.paInt16, output=True, frames_per_buffer=frames_per_buffer)
    stream.write(packed)
    stream.stop_stream()
    stream.close()
    audio.terminate()


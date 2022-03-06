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
import time

import pyaudio
from matplotlib import pyplot as plt

from oscillators import cosine


sample_rate = 22050
scaling = 32500.0
frames_per_buffer = 1024
seed = math.pi

def plot(gen, max_duration=sample_rate * 10, title=None):
    # max_duration is here to save me from the easy mistake of passing in an infinite generator.
    audio = []
    for sig in gen:
        audio.append(sig)
    plt.plot(audio)
    if title != None:
        plt.title(title)
    plt.show()

def play(gen, max_duration=sample_rate * 10):
    # max_duration is here to save me from the easy mistake of passing in an infinite generator.
    audio = array('i')
    for samp in gen:
        audio.append(int( (samp) * scaling))
    packed = struct.pack("<%si" % len(audio), *audio)
    stream = pyaudio.PyAudio().open(rate=sample_rate, channels=1, format=pyaudio.paInt16, output=True, frames_per_buffer=frames_per_buffer)
    stream.write(packed)
    stream.close()


def play_packing_variations():
    # getting the correct values for packing and playing the audio can be a pain - this runs a lot of variations so I can hear what sounds right
    for arrayType in ['i', 'I', 'h', 'H']:
        for offset in [0, 1]:
            for myScale in [32000, 64000, 20000000]:
                for packType in ['<%di', '>%di', '<%dI', '>%dI', '<%dh', '>%dh', '<%dH', '>%dH']:
                    for width in [2]:
                            print("cast to int. arrayType: %s, offset:%d, scale: %d, packType: %s, width: %d" % (arrayType, offset, myScale, packType, width))
                            try:
                                audio = array(arrayType)
                                cos = cosine(200, base_amplitude=1.0, start_phase = math.pi / 2, end_phase = math.pi * 200)
                                for samp in cos:
                                    audio.append(int( (samp + offset) * myScale))
                                packed = struct.pack(packType % len(audio), *audio)
                                play_obj = simpleaudio.play_buffer(packed, 1, width, sample_rate)
                                play_obj.wait_done()
                                time.sleep(0.5)
                            except:
                                pass


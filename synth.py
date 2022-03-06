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

import time
import math
import struct
import threading
from array import array

from pygame import midi
import pyaudio

import shared
import oscillators as osc
import notes
from envelope import up, flat, down, down_30_pct

#This class is a work-in-progress.
#My machine is too slow to supply buffers quick enough to support glitch-free audio output - even with no notes playing!
#Midi needs fixed to loop waiting for connection of a midi keyboard
#run_keyboard needs enhanced to do something interesting with keyboard input

class sequencer():
    def __init__(self):
        self.mutex = threading.Lock()
        self.autonomous = []
        self.releasable = {}

    def run_keyboard(self):
        print("Running keyboard: %s" % threading.get_native_id())
        while True:
            key = input()
            #add some processing here to allow addition of different notes, oscillators, effects, etc...
            if(len(key) > 1):
                with self.mutex:
                    print("Adding gen")
                    self.autonomous.append(notes.striker(osc.square(441), up(duration=0.01), flat(duration=0.2), down(0.5)))

    def run_midi(self):
        print("Running midi: %s" % threading.get_native_id())
        midi.init()
        #this fails before I can use aconnect to wire the keyboard to the process - maybe put in a loop
        mi=midi.Input(device_id=midi.get_default_input_id())
        while True:
            if midi_input.poll():
                print("Midi polled")
                for(status,note,velocity,_),_ in midi_input.read(16):
                    print("Midi event")
                    with self.mutex:
                        if status==0x80:
                            print("Midi release")
                            if(note in self.releasable.keys()):
                                self.releasable[note].release()
                        elif status==0x90:
                            print("Midi press")
                            self.autonomous.append(notes.striker(osc.cosine(midi.midi_to_frequency(notes[key])), up(duration=0.01), flat(duration=0.2), down(0.5)))

    def run_player(self):
        print("Running player: %s" % threading.get_native_id())
        stream = pyaudio.PyAudio().open(rate=shared.sample_rate, channels=1, format=pyaudio.paInt16, output=True, frames_per_buffer=shared.frames_per_buffer)
        audio = array("i")
        #get the audio array up to size before starting to fill with generator output
        for index in range(shared.frames_per_buffer):
            audio.append(int(0))

        dispatch_time = time.perf_counter_ns()
        dispatched_buffer_count = 0

        packed = struct.pack("<%si" % len(audio), *audio)
        while True:
            if len(self.autonomous) == 0 or len(self.releasable) == 0:
                dispatch_time = time.perf_counter_ns()
                dispatched_buffer_count = 0
                time.sleep(shared.frames_per_buffer / shared.sample_rate)
            else:
                for index in range(shared.frames_per_buffer):
                    sig = 0.0
                    len_sigs = 0
                    with self.mutex:
                        delete_releasable_keys = []
                        release_keys = []
                        for generator in self.autonomous:
                            try:
                                sig += next(generator)
                                len_sigs += 1
                            except:
                                pass
                        for key, generator in self.releasable.items():
                            try:
                                sig += next(generator)
                                len_sigs += 1
                            except:
                                delete_releasable_keys.append(key)
                        for key in delete_releasable_keys:
                            del self.releasable['a']
                        for key in release_keys:
                            self.autonomous.append(self.releasable[key])
                            del self.releasable[key]
                    if(len_sigs) > 0:
                        sig = sig / len_sigs
                    audio[index] = int(sig * shared.scaling)
                packed = struct.pack("<%si" % len(audio), *audio)

                elapsed_time = time.perf_counter_ns() - dispatch_time
                dispatched_time = (dispatched_buffer_count * (shared.frames_per_buffer / shared.sample_rate) * 1000000000) 
                print("Elapsed time: %d, dispatched time: %d" % (elapsed_time, dispatched_time))
                if dispatched_time > elapsed_time:
                    print("Ahead by: %d" % (dispatched_time - elapsed_time))
                    time.sleep((dispatched_time - elapsed_time) / 2)
                elif dispatched_time < elapsed_time:
                    print("Behind by: %d after %d dispatched buffers" % (elapsed_time - dispatched_time, dispatched_buffer_count))

                stream.write(packed)
                dispatched_buffer_count += 1


seq = sequencer()
kb = threading.Thread(target=seq.run_keyboard)
pl = threading.Thread(target=seq.run_player)
md = threading.Thread(target=seq.run_midi)
kb.start()
pl.start()
md.start()
kb.join()

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

import util
import shared
import sounds
import factories

#This class is a work-in-progress.
#My machine is too slow to supply buffers quick enough to support glitch-free audio output - even with no notes playing!
#Midi needs fixed to loop waiting for connection of a midi keyboard
#run_keyboard needs enhanced to do something interesting with keyboard input

class sequencer():
    def __init__(self):
        self.mutex = threading.Lock()
        self.releasable = {}
        self.autonomous = []
        self.sound_factory = factories.sound_factory()

    def run_keyboard(self):
        print("Running keyboard: %s" % threading.get_native_id())
        while True:
            key = input()
            #add some processing here to allow addition of different notes, oscillators, effects, etc...
            if(len(key) > 1):
                with self.mutex:
                    pass #do something interesting

    def run_midi(self):
        print("Running midi: %s" % threading.get_native_id())
        midi.init()
        #this fails before I can use aconnect to wire the keyboard to the process - maybe put in a loop

        midi_input = None
        while True:
            try:
                midi_input=midi.Input(device_id=midi.get_default_input_id())
                break
            except midi.MidiException:
                pass
        while True:
            if midi_input.poll():
                #print("Midi polled")
                for(status,note,velocity,other),after in midi_input.read(16):
                    print("Midi event: %s, %s, %s, %s, %s" % (status, note, velocity, other, after))
                    with self.mutex:
                        if status==0x80:
                            #print("Midi chan 1 release")
                            if(note in self.releasable.keys()):
                                self.releasable[note].release()
                        elif status==0x90:
                            #print("Midi chan 1 press")
                            self.releasable[note] = self.sound_factory.produce(note, velocity)
                        elif status==0x99:
                            #print("Midi chan 10 press")
                            self.sound_factory.retool(note)
                        elif status==0xB0 and note==0x01:
                            #print("Midi chan 1 control/mode, mod wheel")
                            self.sound_factory.remodulate(velocity)

    def run_player(self):
        print("Running player: %s" % threading.get_native_id())
        stream = pyaudio.PyAudio().open(rate=shared.sample_rate, channels=1, format=pyaudio.paInt16, output=True, frames_per_buffer=shared.frames_per_buffer)
        audio = array("i")
        #get the audio array up to size before starting to fill with generator output
        for index in range(shared.frames_per_buffer):
            audio.append(int(0))

        dispatched_buffer_count = 0
        dispatch_time = time.perf_counter_ns()

        while True:
            #print("Once more round the sun")
            delete_releasable_keys = []
            delete_autonomous = []

            if (len(self.releasable) == 0) and (len(self.autonomous) == 0):
                time.sleep(shared.frames_per_buffer / shared.sample_rate)
                dispatched_buffer_count = 0
                dispatch_time = time.perf_counter_ns()
            else:
                #print("%d releasable, %d autonomous" % (len(self.releasable), len(self.autonomous)))
                with self.mutex:
                    for index in range(shared.frames_per_buffer):
                        sig = 0.0
                        len_sigs = 0

                        for generator in self.autonomous:
                            if generator not in delete_autonomous:
                                try:
                                    #print("Value from autonomous")
                                    sig += next(generator)
                                    len_sigs += 1
                                except StopIteration:
                                    delete_autonomous.append(generator)

                        for key, generator in self.releasable.items():
                            if key not in delete_releasable_keys:
                                try:
                                    #print("Value from releasable")
                                    sig += next(generator)
                                    len_sigs += 1
                                except StopIteration:
                                    delete_releasable_keys.append(key)

                        if(len_sigs) > 0:
                            sig = sig / len_sigs
                            #print("SIG: %f" % sig)
                        audio[index] = int(sig * shared.scaling)

                    #print("Count of releasable to remove: %d" % len(delete_releasable_keys))
                    for key in delete_releasable_keys:
                        #print("Removing: %s" % key)
                        del self.releasable[key]

                    #print("Count of autonomous to remove: %d" % len(delete_autonomous))
                    for gen in delete_autonomous:
                        #print("Removing: %s" % gen)
                        self.autonomous.remove(gen)

                packed = struct.pack("<%si" % len(audio), *audio)
                #print("before stream write")
                stream.write(packed)
                #print("after stream write")
                dispatched_buffer_count += 1

                elapsed_time = time.perf_counter_ns() - dispatch_time
                dispatched_time = (dispatched_buffer_count * (shared.frames_per_buffer / shared.sample_rate) * 1000000000) 
                #print("Elapsed time: %d, dispatched time: %d" % (elapsed_time, dispatched_time))
                if dispatched_time > elapsed_time:
                    pass
                    #print("Ahead by: %d" % (dispatched_time - elapsed_time))
                    #print("Sleep for: %f" % ((dispatched_time - elapsed_time) / (2 * 1000000000)))
                    #time.sleep((dispatched_time - elapsed_time) / (2 * 1000000000))
                elif dispatched_time < elapsed_time:
                    pass
                    #print("Behind by: %d after %d dispatched buffers" % (elapsed_time - dispatched_time, dispatched_buffer_count))
                #print("here 1")
            #print("here 2")
        #print("here 3")



seq = sequencer()
kb = threading.Thread(target=seq.run_keyboard)
pl = threading.Thread(target=seq.run_player)
md = threading.Thread(target=seq.run_midi)
kb.start()
pl.start()
md.start()
kb.join()

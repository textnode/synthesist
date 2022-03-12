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

import threading

from pygame import midi

class midi_monitor():
    def __init__(self):
        self.mutex = threading.Lock()

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
                            print("Midi release")
                        elif status==0x90:
                            print("Midi press")


mm = midi_monitor()
md = threading.Thread(target=mm.run_midi)
md.start()
md.join()

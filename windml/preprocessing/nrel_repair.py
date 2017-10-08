"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from numpy import zeros, float32, int32
from builtins import range

class NRELRepair(object):
    def repair(self, measurements):
        distances = self.get_distances(measurements)
        timesteps = 600

        jumpsto_index = {}
        jumpers = []
        for i, d in enumerate(self.get_distances(measurements)):
            if(d != timesteps):
                jumper = i
                jumper_date = measurements[i]['date']
                found = False
                for k in range(i+1, measurements.shape[0]):
                    if(measurements[k]['date'] == jumper_date):
                        found = True                           
                        jumpsto = k
                if not found:
                    import pdb
                    pdb.set_trace()
                    raise Exception("Data is missing, repairing impossible.")
                jumpers.append((jumper, jumpsto))
                jumpsto_index[jumper] = jumpsto

        new_amount = measurements.shape[0]
        for jumper, jumpsto in jumpers:
            new_amount -= (jumpsto - jumper) 

        # allocate new numpy array
        filled = zeros((new_amount,), dtype=[('date', int32),\
                ('corrected_score', float32),\
                ('speed', float32)])

        new_index = 0
        old_index = 0 
        keys = jumpsto_index.keys()
        while old_index < measurements.shape[0]:
            if(old_index in keys):
                old_index = jumpsto_index[old_index] 
            else:
                filled[new_index] = measurements[old_index]
                new_index += 1
                old_index += 1

        return filled 

    def get_distances(self, measurements):
        distances = []
        for i in range(len(measurements) - 1):
            d = measurements[i]['date']
            dn = measurements[i + 1]['date']
            distances.append(dn - d)
        return distances

    def validate(self, measurements):
        timesteps = 600
        valid = True
        for i, d in enumerate(self.get_distances(measurements)):
            if(d != timesteps):
                print("Wrong distance %i at index %i" % (d, i))
                valid = False
                import pdb
                pdb.set_trace()

        return valid 


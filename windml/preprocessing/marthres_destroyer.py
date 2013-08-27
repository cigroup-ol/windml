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

from random import randint
from math import floor
from numpy import zeros, float32, int32

class MARThresDestroyer(object):
    def destroy(self, timeseries, **args):
        percentage = args['percentage']
        lower_bound = args['lower_bound']
        upper_bound = args['upper_bound']

        lseries = timeseries.shape[0]
        marked_indices = []
        remove_indices = []

        old_index = 0
        while old_index < lseries:
            lb = timeseries[old_index]['corrected_score'] < lower_bound
            ub = timeseries[old_index]['corrected_score'] > upper_bound
            if(lb or ub):
                marked_indices.append(old_index)
            old_index += 1

        if(len(marked_indices) == 0):
            raise Exception("No data met criteria")

        amount_remove = int(floor(len(marked_indices) * percentage))
        removed = 0
        while removed < amount_remove:
            x = randint(0, len(marked_indices) - 1)
            remove_indices.append(marked_indices[x])
            marked_indices.remove(marked_indices[x])
            removed += 1
        new_amount = lseries - len(remove_indices)

        # allocate new numpy array
        new_mat = zeros((new_amount,), dtype=[('date', int32),\
                ('corrected_score', float32),\
                ('speed', float32)])

        index_old = 0
        index_new = 0
        while index_old < lseries:
            if(index_old in remove_indices):
                index_old += 1
            else:
                new_mat[index_new] = timeseries[index_old]
                index_old += 1
                index_new += 1

        return new_mat

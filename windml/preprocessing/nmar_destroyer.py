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
from numpy import zeros, float32, int32, nan

class NMARDestroyer(object):
    def destroy(self, timeseries, **args):
        percentage = args['percentage']
        min_length = args['min_length']
        max_length = args['max_length']

        lseries = timeseries.shape[0]
        marked = 0
        marked_intervals = []
        while(marked < int(floor((lseries * percentage)))):
            start = randint(0, lseries - 1)
            end = randint(start + min_length, start + max_length)
            while(end > lseries - 1):
                start = randint(0, lseries - 1)
                end = randint(start + min_length, start + max_length)
            marked += (end - start)
            marked_intervals.append((start, end))

        exceptions = [0, lseries - 1]

        # exclude indices
        if('exclude' in args.keys()):
            exceptions = exceptions + args['exclude']

        removed_indices = []
        index_old = 0
        while index_old < lseries:
            for interval in marked_intervals:
                (start, end) = interval
                if((start <= index_old <= end) and index_old not in exceptions):
                    removed_indices.append(index_old)
                    break
            index_old += 1

        new_amount = lseries - len(removed_indices)
        # allocate new numpy array
        new_mat = zeros((new_amount,), dtype=[('date', int32),\
                ('corrected_score', float32),\
                ('speed', float32)])

        index_old = 0
        index_new = 0
        while index_old < lseries:
            if(index_old in removed_indices):
                index_old += 1
            else:
                new_mat[index_new] = timeseries[index_old]
                index_old += 1
                index_new += 1

        return new_mat, removed_indices

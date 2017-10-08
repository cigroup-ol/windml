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
from past.builtins import range

class MARDestroyer(object):
    def destroy(self, timeseries, **args):
        percentage = args['percentage']

        lseries = timeseries.shape[0]
        remove_indices = []
        amount_remove = int(floor(lseries * percentage))
        new_amount = lseries - amount_remove

        # allocate new numpy array
        newmat = zeros((new_amount,), dtype=[('date', int32),\
                ('corrected_score', float32),\
                ('speed', float32)])

        # first and last element must not be deleted, because
        # the interpolated has to have the same length.
        exceptions = [0, lseries - 1]

        # exclude indices
        if 'exclude' in args.keys():
            exceptions = exceptions + args['exclude']

        indices = range(0, timeseries.shape[0])
        for exception in exceptions:
            indices.remove(exception)

        for i in range(amount_remove):
            x = randint(0, len(indices) - 1)
            remove_indices.append(indices[x])
            indices.remove(indices[x])

        current = 0
        for i in range(lseries):
            if i not in remove_indices:
                newmat[current] = timeseries[i]
                current += 1

        return newmat, remove_indices

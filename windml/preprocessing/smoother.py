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

from numpy import zeros, int32, float32

class Smoother(object):
    def smooth(self, timeseries, args):
        ilen = args['interval_length']

        new_amount = timeseries.shape[0]
        smoothed_ts = zeros((new_amount,), dtype=[('date', int32),\
                ('corrected_score', float32),\
                ('speed', float32)])

        if(ilen % 2 == 0 or ilen == 1):
            raise Exception("interval length must be odd and not 1.")

        padding = int((ilen - 1) / 2.0)

        # copy data in the beginning and the end cannot be smoothed
        # because of padding
        for i in range(0, padding):
            smoothed_ts[i] = timeseries[i] # copy old data
        for i in range(len(timeseries) - padding, len(timeseries)):
            smoothed_ts[i] = timeseries[i] # copy old data

        # smooth data
        for i in range(padding, len(timeseries) - padding):
            sp_mean = timeseries[(i - padding):(i + padding)]['speed'].mean()
            cs_mean = timeseries[(i - padding):(i + padding)]['corrected_score'].mean()

            smoothed_ts[i] = timeseries[i] # copy old data
            smoothed_ts[i]['corrected_score'] = cs_mean
            smoothed_ts[i]['speed'] = sp_mean

        return smoothed_ts

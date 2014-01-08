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

from testbeds import NREL_4_parks, QuickNDirty
from numpy import arange
import matplotlib.pyplot as plt
from windml.visualization.colorset import colorset

class Benchmark():

    testbeds = {'NREL_4_parks' : NREL_4_parks,
                'QuickNDirty' : QuickNDirty}
    results = {}

    def _mse(self, y_hat, y_test):
        mse_y_hat = 0
        for i in range(0, len(y_hat)):
            mse_y_hat += (y_hat[i] - y_test[i]) ** 2

        return (1.0/len(y_hat)) * mse_y_hat

    def run(self, regressor, testbed_name, parallel=False):
        parks = self.testbeds[testbed_name]()

        def run_park(job):
            park, testbed = job
            wp_train, wp_test = testbed

            regressor.fit(wp_train)
            y_hat, y_test = regressor.predict(wp_test)

            statistics = {'mse': self._mse(y_hat, y_test)}
            return {'park' : park, 'statistics' : statistics}

        jobs = []
        for k, v in parks.iteritems():
            jobs.append((k,v))

        # parallel
        if(parallel == True):
            from playdoh import map as pmap
            from multiprocessing import cpu_count
            cpus = cpu_count()
            self.results[regressor] = pmap(run_park, jobs, cpu = cpus)
        else:
            # sequential
            self.results[regressor] = map(run_park, jobs)

        return self.results

    def print_results(self):
        for regressor, rresults in self.results.iteritems():
            print "Results for regressor %s" % str(regressor)
            for rresult in rresults:
                park = rresult['park']
                statistics = rresult['statistics']
                print "%s MSE: %f" % (park, statistics['mse'])

    def visualize_mse_on_parks(self):
        index = arange(len(self.results[self.results.keys()[0]]))
        bar_width = 0.3

        current_bar = 0
        for regressor, rresults in self.results.iteritems():

            park_names = []
            mses = []

            for result in rresults:
                park = result['park']
                park_names.append(park)
                mse = result['statistics']['mse']
                mses.append(mse)

            rects1 = plt.bar(index + current_bar * bar_width,
                         mses,
                         bar_width,
                         color=colorset[current_bar],
                         label=regressor.__class__.__name__)

            current_bar = current_bar + 1

        plt.xlabel('Park')
        plt.ylabel('MSE [MW]')
        plt.title('MSE [MW] by Park')

        plt.xticks(index + (current_bar * bar_width) / 2.0,\
                   park_names)
        plt.legend()

        plt.tight_layout()
        plt.show()


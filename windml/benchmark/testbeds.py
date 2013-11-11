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

def NREL_4_parks():
    """ Four parks, with 5 km radius, 2 years, horizon and feature
        window equals 30 minutes."""

    from windml.datasets.nrel import NREL
    from windml.preprocessing.preprocessing import repair_nrel

    parks = {'palmsprings' : 1175,
             'reno' : 11637,
             'casper' : 23167,
             'carway' : 30498}

    testbed = {}

    # return X,y tuples
    for park in parks.keys():

        # training data ----
        windpark_train = NREL().get_windpark_nearest(parks[park], 5, 2004)
        target = windpark_train.get_target()

        # repair NREL data
        turbines = windpark_train.get_turbines()
        for t in range(len(turbines)):
            turbines[t].add_measurements(\
                repair_nrel(turbines[t].get_measurements()[:39457]))

        # test data ----
        windpark_test = NREL().get_windpark_nearest(parks[park], 5, 2005)
        target = windpark_test.get_target()

        # repair NREL data
        turbines = windpark_test.get_turbines()
        for t in range(len(turbines)):
            turbines[t].add_measurements(\
                repair_nrel(turbines[t].get_measurements()[:39457]))

        testbed[park] = (windpark_train, windpark_test)

    return testbed

def QuickNDirty():
    """ Four parks, with 5 km radius, 2 years, horizon and feature
        window equals 30 minutes."""

    from windml.datasets.nrel import NREL
    from windml.preprocessing.preprocessing import repair_nrel

    parks = {'palmsprings' : 1175,
             'reno' : 11637}

    testbed = {}

    # return X,y tuples
    for park in parks.keys():

        # training data ----
        windpark_train = NREL().get_windpark_nearest(parks[park], 5, 2004)
        target = windpark_train.get_target()

        # repair NREL data
        turbines = windpark_train.get_turbines()
        for t in range(len(turbines)):
            turbines[t].add_measurements(\
                repair_nrel(turbines[t].get_measurements()[:3457]))

        # test data ----
        windpark_test = NREL().get_windpark_nearest(parks[park], 5, 2005)
        target = windpark_test.get_target()

        # repair NREL data
        turbines = windpark_test.get_turbines()
        for t in range(len(turbines)):
            turbines[t].add_measurements(\
                repair_nrel(turbines[t].get_measurements()[:3457]))

        testbed[park] = (windpark_train, windpark_test)

    return testbed



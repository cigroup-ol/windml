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

from __future__ import print_function
from builtins import range
from numpy.random import normal, rand

class OnePlusOneEA(object):

    def minimize(self, parameter, mean, sigma, interval, iterations, args, algorithm):
        """
        A (1+1)-EA for real parameter optimization of an algorithm. Does
        not adapt step size, the choice of sigma is therefore very important.

        parameter: the name of the real parameter to minimize
        mean: mean of population and start position respectively
        sigma: step size of the evolution process
        interval: feasible interval of parameter solutions
        iterations: how many iteration until termination
        args: hashmap of the arguments of algorithm
        algorithm: the algorithm function to optimize, the function
        needs to accept the args hashmap.

        Example: Optimizing a custom algorithm
        --------------------------------------------

        def algorithm(args):
            # here return the error to minimize
            return args['radius'] ** 2

        args = {'otherarg' : 1}
        inte = [0, 10]
        optradius, error = minimize11ea('radius', 1.0, 5.0, inte, 50, args, algorithm)
        """

        feasible = False
        while(not feasible):
            parent = normal(mean, sigma)
            if(interval[0] <= parent <= interval[1]):
                print(parent)
                feasible = True

        args[parameter] = parent
        best_error = algorithm(args)

        for i in range(iterations):
            feasible = False
            while(not feasible):
                offspring = parent + normal(mean, sigma)
                if(interval[0] <= offspring <= interval[1]):
                    print(offspring)
                    feasible = True
            args[parameter] = offspring
            error = algorithm(args)
            if(error < best_error):
                parent = offspring
                best_error = error
                print(parent, error)

        return parent, best_error


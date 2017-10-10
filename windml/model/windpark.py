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

import math
import numpy as np
import datetime
import time


class Windpark(object):
    """The class Windpark represents a park, which consists of
    one or more turbines."""

    def __init__(self, target_idx, radius):
        """Initializes windpark with a given target id and radius.

        Parameters
        ----------
        target_idx : int
                     A user-defined id.
        radius : int
                 A radius around the target in km.
        """

        self.target_idx = target_idx
        self.radius = radius
        self.turbines = []

    def get_target_idx(self):
        """Get target id.

        Returns
        -------
        target_idx : int
                     A user-defined id.
        """
        return self.target_idx

    def get_target(self):
        """Get target.

        Returns
        -------
        Turbine
            Target turbine.
        """

        return self.turbines[len(self.turbines) - 1]

    def add_turbine(self, turbine):
        """Adds a turbine to the windpark.

        Parameters
        ----------
        turbine : Turbine
               Turbine to add.
        """

        self.turbines.append(turbine)

    def get_turbines(self):
        """Get all turbines from park.

        Returns
        -------
        array
            Array of all turbines.
        """

        return self.turbines

    def get_radius(self):
        """Get radius of windpark relative to the target turbine.

        Returns
        -------
        int
            Radius in km.
        """

        return self.radius

    def get_powermatrix(self):
        """Get the power matrix of all turbines. A power matrix consists of
        all corrected_scores.

        Returns
        -------
        numpy.matrix
            Matrix, rows are time steps, columns are correct_scores of each
            turbine.
        """

        num_m = len(self.turbines[0].measurements)
        num_turbines = len(self.turbines)

        p_matrix = [[0 for col in range(num_turbines)] for row in range(num_m)]
        for f in range(num_turbines):
            for time in range(num_m):
                p_matrix[time][f] = self.turbines[f].measurements[time][1]

        p_matrix = np.array(p_matrix)
        return p_matrix

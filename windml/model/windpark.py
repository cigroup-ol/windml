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
import datetime, time

class Windpark(object):
    """The class Windpark represents a park, which consists of
    one or more windmills."""

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
        self.mills = []

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
        Windmill
            Target windmill.
        """

        return self.mills[len(self.mills)-1]

    def add_windmill(self, mill):
        """Adds a windmill to the windpark.

        Parameters
        ----------
        mill : Windmill
               Windmill to add.
        """

        self.mills.append(mill)

    def get_windmills(self):
        """Get all windmills from park.

        Returns
        -------
        array
            Array of all windmills.
        """

        return self.mills

    def get_radius(self):
        """Get radius of windpark relative to the target windmill.

        Returns
        -------
        int
            Radius in km.
        """

        return self.radius

    def get_powermatrix(self):
        """Get the power matrix of all wind mills. A power matrix consists of
        all corrected_scores.

        Returns
        -------
        numpy.matrix
            Matrix, rows are time steps, columns are correct_scores of each
            mill.
        """

        num_m = len(self.mills[0].measurements)
        num_mills = len(self.mills)

        p_matrix = [[0 for col in range(num_mills)] for row in range(num_m)]
        for f in range(num_mills):
            for time in range(num_m):
                p_matrix[time][f] = self.mills[f].measurements[time][1]

        p_matrix = np.array(p_matrix)
        return p_matrix


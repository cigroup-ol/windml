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

from numpy import zeros, float32
from windml.mapping.mapping import Mapping

cs = 'speed'

class SpeedMapping(Mapping):
    """Maps time series to feature-label pairs, use speed"""

    def get_features_turbine(self, turbine, feature_window, horizon, padding = 0):
        """Get features from a given turbine, consisting of the values of the
        speed of a turbine depending on feature_window size and time
        horizon and optionally a certain padding.

        Parameters
        ----------
        turbine : Turbine
                   Features of the given turbine.
        feature_window : int
                         The amount of time steps of the feature window.
        horizon: int
                 The amount of time steps of the horizon.

        Returns
        -------
        numpy.matrix
            Pattern matrix for regression.
        """

        timesteps = len(turbine.measurements) - (feature_window + horizon + padding - 1)

        features = zeros((timesteps, feature_window), dtype = float32)
        for t in range(padding, timesteps):
            features[t][0:feature_window] =\
                    turbine.measurements[cs][t:t + feature_window]

        return features

    def get_labels_turbine(self, turbine, feature_window, horizon, padding = 0):
        """Get labels for a given turbine, consisting of the values of the
        speed for one turbine depending on feature window, horizon and
        optionally a certain padding.

        Parameters
        ----------
        turbine : Turbine
                   Features of the given turbine.
        feature_window : int
                         The amount of time steps of the feature window.
        horizon: int
                 The amount of time steps of the horizon.

        Returns
        -------
        numpy.array
            Label array for regression.
        """

        timesteps = len(turbine.measurements) - (feature_window + horizon + padding - 1)

        labels = zeros(timesteps, dtype = float32)
        for t in range(padding, timesteps):
            offset = t + feature_window + horizon - 1
            labels[t] = turbine.measurements[cs][offset]

        return labels

    def get_features_park(self, windpark, feature_window, horizon, padding = 0):
        """Get features for a given windpark, consisting of the values of the
        speed for all turbines in the park depending on feature_window
        size and time horizon and optionally a certain padding.

        Parameters
        ----------
        windpark : Windpark
                   Features of the given windpark.
        feature_window : int
                         The amount of time steps of the feature window.
        horizon: int
                 The amount of time steps of the horizon.

        Returns
        -------
        numpy.matrix
            Pattern matrix for regression.
        """

        turbines = windpark.get_turbines()
        amount = len(turbines)
        timesteps = len(turbines[0].measurements) - (feature_window + horizon + padding - 1)

        features = zeros((timesteps, amount * feature_window), dtype = float32)

        for idx, turbine in enumerate(turbines):
            for t in range(padding, timesteps):
                startc = idx * feature_window
                endc = (idx + 1) * feature_window
                features[t][startc:endc] = turbine.measurements[cs][t:t + feature_window]

        return features

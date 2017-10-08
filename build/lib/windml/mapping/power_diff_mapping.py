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

cs = 'corrected_score'

class PowerDiffMapping(Mapping):
    """Maps time series to feature-label pairs, use power and differences"""

    def get_features_turbine(self, turbine, feature_window, horizon, padding = 0):
        """Get features from a given turbine, consisting of the values of the
        corrected score and their corresponding changes for one turbine dependend
        on feature_window size and time horizon and optionally a certain
        padding.

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
        num_features = 2 * feature_window - 1

        measurements = turbine.measurements[cs]
        features = zeros((timesteps, num_features), dtype = float32)
        for t in range(padding, timesteps):
            for i in range(feature_window):
                features[t][i]=measurements[t+i]
                if i!=0:
                    features[t][feature_window+i-1] = measurements[t+i]-measurements[t+i-1]

        return features

    def get_labels_turbine(self, turbine, feature_window, horizon, padding = 0):
        """Get labels for a given turbine, consisting of the values of the
        corrected score for one turbine dependend on feature window, horizon and
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
        corrected score and their corresponding changes for all turbines in the
        park dependend on feature_window size and time horizon and optionally a
        certain padding.

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

        num_features = 2 * feature_window - 1
        features = zeros((timesteps, amount * num_features), dtype = float32)

        for idx, turbine in enumerate(turbines):
            measurements = turbine.measurements[cs]
            for t in range(padding, timesteps):
                for i in range(feature_window):
                    features[t][idx * feature_window + i] = measurements[t+i]
                    if i!=0:
                        start_diffs = amount * feature_window
                        diff_offset = (feature_window - 1) * idx + i - 1
                        features[t][start_diffs + diff_offset] = measurements[t+i]-measurements[t+i-1]

        return features

    def get_labels_park(self, windpark, feature_window, horizon, padding = 0):
        """Get labels for a given windpark, consisting of the values of the
        corrected score for all turbines in the park dependend on feature window,
        horizon and optionally a certain padding. The labels are the sums of
        the corrected score of all turbines in the park.

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
        numpy.array
            Label array for regression.
        """

        turbines = windpark.get_turbines()
        timesteps = len(turbines[0].measurements) - (feature_window + horizon + padding - 1)

        sum_turbines = zeros(timesteps, dtype = float32)
        for turbine in turbines:
            for t in range(padding, timesteps):
                sum_turbines[t] += turbine.measurements[cs][t + feature_window + horizon - 1]

        return sum_turbines


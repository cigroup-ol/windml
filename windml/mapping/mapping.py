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

class Mapping(object):
    """Maps time series to feature-label pairs"""

    def get_features_mill(self, windmill, feature_window, horizon, padding):
        """Get features from a given windmill dependend on feature_window size
        and time horizon and optionally a certain padding.

        Parameters
        ----------
        windmill : Windmill
                   Features of the given windmill.
        feature_window : int
                         The amount of time steps of the feature window.
        horizon: int
                 The amount of time steps of the horizon.

        Returns
        -------
        numpy.matrix
            Pattern matrix for regression.
        """
        pass

    def get_features_park(self, windpark, feature_window, horizon, padding):
        """Get features for a given windpark dependend on feature_window size
        and time horizon and optionally a certain padding.

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
        pass

    def get_labels_mill(self, windmill, feature_window, horizon, padding):
        """Get labels for a given windmill, dependend on feature window,
        horizon and optionally a certain padding.

        Parameters
        ----------
        windmill : Windmill
                   Features of the given windmill.
        feature_window : int
                         The amount of time steps of the feature window.
        horizon: int
                 The amount of time steps of the horizon.

        Returns
        -------
        numpy.array
            Label array for regression.
        """
        pass

    def get_labels_park(self, windmill, feature_window, horizon, padding):
        """Get labels for a given windpark dependend on feature window, horizon
        and optionally a certain padding. The labels are the sums of the
        corrected score of all windmills in the park.

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
        pass

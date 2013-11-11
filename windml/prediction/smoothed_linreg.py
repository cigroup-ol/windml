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

from sklearn import linear_model
from windml.mapping.power_mapping import PowerMapping
from windml.preprocessing.preprocessing import smoothen
from windml.visualization.colorset import colorset

class SmoothedLinreg():
    """ Standard spatio-temporal model with smoothing preprocessing,
        PowerMapping and linear regression. """

    def __init__(self, smooth=3):
        self.model = linear_model.LinearRegression()
        self.feature_window = 3
        self.horizon = 3
        self.smooth = smooth

    def fit(self, wp_train):
        target = wp_train.get_target()

        # smoothing of all time series
        turbines = wp_train.get_turbines()
        for turbine in turbines:
            turbine.add_measurements(\
                smoothen(turbine.get_measurements(), interval_length=self.smooth))

        mapping = PowerMapping()
        X_train = mapping.get_features_park(wp_train, self.feature_window, self.horizon)
        y_train = mapping.get_labels_turbine(target, self.feature_window, self.horizon)

        self.model.fit(X_train, y_train)

    def predict(self, wp_test):
        target = wp_test.get_target()
        mapping = PowerMapping()
        X_test = mapping.get_features_park(wp_test, self.feature_window, self.horizon)
        y_test = mapping.get_labels_turbine(target, self.feature_window, self.horizon)

        return self.model.predict(X_test), y_test



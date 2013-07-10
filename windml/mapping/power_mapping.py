from numpy import zeros, float32
from windml.mapping.mapping import Mapping

cs = 'corrected_score'

class PowerMapping(Mapping):
    """Maps time series to feature-label pairs, use power"""

    def get_features_mill(self, windmill, feature_window, horizon, padding = 0):
        """Get features from a given windmill, consisting of the values of the
        corrected score for one mill dependend on feature_window size and time
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
        numpy.matrix
            Pattern matrix for regression.
        """

        timesteps = len(windmill.measurements) - (feature_window + horizon + padding - 1)

        features = zeros((timesteps, feature_window), dtype = float32)
        for t in range(padding, timesteps):
            features[t][0:feature_window] =\
                    windmill.measurements[cs][t:t + feature_window]

        return features

    def get_labels_mill(self, windmill, feature_window, horizon, padding = 0):
        """Get labels for a given windmill, consisting of the values of the
        corrected score for one mill dependend on feature window, horizon and
        optionally a certain padding.

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

        timesteps = len(windmill.measurements) - (feature_window + horizon + padding - 1)

        labels = zeros(timesteps, dtype = float32)
        for t in range(padding, timesteps):
            offset = t + feature_window + horizon - 1
            labels[t] = windmill.measurements[cs][offset]

        return labels

    def get_features_park(self, windpark, feature_window, horizon, padding = 0):
        """Get features for a given windpark, consisting of the values of the
        corrected score for all mills in the park dependend on feature_window
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

        mills = windpark.get_windmills()
        amount = len(mills)
        timesteps = len(mills[0].measurements) - (feature_window + horizon + padding - 1)

        features = zeros((timesteps, amount * feature_window), dtype = float32)

        for idx, mill in enumerate(mills):
            for t in range(padding, timesteps):
                startc = idx * feature_window
                endc = (idx + 1) * feature_window
                features[t][startc:endc] = mill.measurements[cs][t:t + feature_window]

        return features

    def get_labels_park(self, windpark, feature_window, horizon, padding = 0):
        """Get labels for a given windpark, consisting of the values of the
        corrected score for all mills in the park dependend on feature window,
        horizon and optionally a certain padding. The labels are the sums of
        the corrected score of all windmills in the park.

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

        mills = windpark.get_windmills()
        timesteps = len(mills[0].measurements) - (feature_window + horizon + padding - 1)

        sum_mills = zeros(timesteps, dtype = float32)
        for mill in mills:
            for t in range(padding, timesteps):
                sum_mills[t] += mill.measurements[cs][t + feature_window + horizon - 1]

        return sum_mills


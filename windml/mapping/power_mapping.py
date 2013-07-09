from numpy import zeros, float32
from windml.mapping.mapping import Mapping

cs = 'corrected_score'

class PowerMapping(Mapping):
    """Maps time series to feature-label pairs, use power"""

    def get_features_mill(self, windmill, feature_window, horizon, padding = 0):
        timesteps = len(windmill.measurements) - (feature_window + horizon + padding - 1)

        features = zeros((timesteps, feature_window), dtype = float32)
        for t in range(padding, timesteps):
            features[t][0:feature_window] =\
                    windmill.measurements[cs][t:t + feature_window]

        return features

    def get_labels_mill(self, windmill, feature_window, horizon, padding = 0):
        timesteps = len(windmill.measurements) - (feature_window + horizon + padding - 1)

        labels = zeros(timesteps, dtype = float32)
        for t in range(padding, timesteps):
            offset = t + feature_window + horizon - 1
            labels[t] = windmill.measurements[cs][offset]

        return labels

    def get_features_park(self, windpark, feature_window, horizon, padding = 0):

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
        mills = windpark.get_windmills()
        timesteps = len(mills[0].measurements) - (feature_window + horizon + padding - 1)

        sum_mills = zeros(timesteps, dtype = float32)
        for mill in mills:
            for t in range(padding, timesteps):
                sum_mills[t] += mill.measurements[cs][t + feature_window + horizon - 1]

        return sum_mills


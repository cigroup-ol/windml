from numpy import zeros, float32
from windml.mapping.mapping import Mapping

cs = 'corrected_score'

class PowerDiffMapping(Mapping):
    """Maps time series to feature-label pairs, use power and differences"""

    def get_features_mill(self, windmill, feature_window, horizon, padding = 0):
        timesteps = len(windmill.measurements) - (feature_window + horizon + padding - 1)
        num_features = 2 * feature_window - 1

        measurements = windmill.measurements[cs]
        features = zeros((timesteps, num_features), dtype = float32)
        for t in range(padding, timesteps):
            for i in range(feature_window):
                features[t][i]=measurements[t+i]
                if i!=0:
                    features[t][feature_window+i-1] = measurements[t+i]-measurements[t+i-1]

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

        num_features = 2 * feature_window - 1
        features = zeros((timesteps, amount * num_features), dtype = float32)

        for idx, mill in enumerate(mills):
            measurements = mill.measurements[cs]
            for t in range(padding, timesteps):
                for i in range(feature_window):
                    features[t][idx * feature_window + i] = measurements[t+i]
                    if i!=0:
                        start_diffs = amount * feature_window
                        diff_offset = (feature_window - 1) * idx + i - 1
                        features[t][start_diffs + diff_offset] = measurements[t+i]-measurements[t+i-1]

        return features

    def get_labels_park(self, windpark, feature_window, horizon, padding = 0):
        mills = windpark.get_windmills()
        timesteps = len(mills[0].measurements) - (feature_window + horizon + padding - 1)

        sum_mills = zeros(timesteps, dtype = float32)
        for mill in mills:
            for t in range(padding, timesteps):
                sum_mills[t] += mill.measurements[cs][t + feature_window + horizon - 1]

        return sum_mills


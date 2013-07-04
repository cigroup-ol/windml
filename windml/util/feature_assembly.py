from numpy import array

### methods, add new custom methods here.

def method_corrected_score(fa, feature_window, horizon, weights):
    ftimesteps = len(fa.data) - (feature_window + horizon - 1)
    lis = fa.all_features(weights, 0, ftimesteps, feature_window)
    return array(map(lambda li : reduce(lambda x, y : x + y, li), lis))

def method_corrected_score_and_diffs(fa, feature_window, horizon, weights):
    ftimesteps = len(fa.data) - (feature_window + horizon - 1)
    lis = map(lambda s, e : fa.feature_vector(weights, s, e) + fa.diff_vector(weights, s, e),
        xrange(0, ftimesteps),
        xrange(0 + feature_window, ftimesteps + feature_window))
    return array(map(lambda li : reduce(lambda x, y : x + y, li), lis))

def method_diffs(fa):
    return []

class FeatureAssembly(object):

    _methods = {
        'corrected_score': method_corrected_score,
        'corrected_score_and_diffs': method_corrected_score_and_diffs,
        'diffs': method_diffs
    }

    def __init__(self, windmills):
        self.amount = len(windmills)
        self.timesteps = len(windmills[0].measurements)

        self.data = array(map(lambda t :\
            map(lambda wm : wm.measurements[t][1], windmills),\
            xrange(self.timesteps)))

    def feature_window(self, wmi, wmi_factor, start, end):
        return map(lambda t : wmi_factor * self.data[t][wmi], xrange(start, end))

    def feature_vector(self, wmi_factors, start, end):
        return map(self.feature_window,\
                xrange(self.amount),\
                wmi_factors,\
                [start] * self.amount,\
                [end] * self.amount)

    def all_features(self, wmi_factors, start, end, window):
        return map(self.feature_vector,\
            [wmi_factors] * (end - start),
            xrange(start, end),\
            xrange(start + window, end + window))

    def diff_window(self, wmi, wmi_factor, start, end):
        return map(lambda t : wmi_factor * (self.data[t][wmi] - self.data[t-1][wmi]),\
            xrange(start + 1, end))

    def diff_vector(self, wmi_factors, start, end):
        return map(self.diff_window,\
            xrange(self.amount),
            wmi_factors,\
            [start] * self.amount,
            [end] * self.amount)

    def all_diffs(self, wmi_factors, start, end, window):
        return map(self.diff_vector,\
            [wmi_factors] * (end - start),
            xrange(start, end),
            xrange(start + window, end + window))

    def X(self, method, feature_window, horizon, weights=False):
        if not weights:
            weights = [1.0] * self.amount
        func = self._methods[method]
        return func(self, feature_window, horizon, weights)

    def Y(self, target, feature_window, horizon):
        ftimesteps = len(self.data) - (feature_window + horizon - 1)
        li = map(\
            lambda t : target.measurements[t + feature_window + horizon - 1][1],\
            xrange(ftimesteps))
        return array(li)



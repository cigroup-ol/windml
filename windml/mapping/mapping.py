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

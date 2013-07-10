class DataSource(object):
    """Abstract class of data sources"""

    def get_windpark(self, target_idx, radius, year_from=0, year_to=0):
        """This method returns a Windpark object of a given data source.

        Parameters
        ----------

        target_idx : int
                     Depends on the data source.
        year_from  : int
                     2004 - 2006
        year_to    : int
                     2004 - 2006

        Returns
        -------

        Windpark
            An according windpark for target id, radius and time span.
        """
        pass

    def get_windmill(self, target_idx, year_from=0, year_to=0):
        """This method returns a Windmill object of a given data source.

        Parameters
        ----------

        target_idx : int
                     Depends on the data source.
        year_from  : int
                     2004 - 2006
        year_to    : int
                     2004 - 2006

        Returns
        -------

        Windmill
            An according windmill for target id and time span.
        """
        pass


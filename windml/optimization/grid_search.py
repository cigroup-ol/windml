from windml.util.logger import Logger
from playdoh import map as pmap
from multiprocessing import cpu_count

class GridSearch(object):

    def __init__(self):
        self.logger = Logger(self)

    def _run_value(self, value, parameter, args, algorithm):
        args[parameter] = value
        error = algorithm(args)
        return (value, error)

    def minimize(self, parameter, interval, stepsize, args, algorithm, parallel=True):
        """
        Example: Optimizing a custom algorithm with GridSearch
        ------------------------------------------------------

        def algorithm(args):
            # here return the error to minimize
            return args['radius'] ** 2

        args = {'otherarg' : 1}
        inte = [0, 10]
        step = 1
        optradius, error = minimize11ea('radius', inte, step, args, algorithm)
        """

        diff = interval[1] - interval[0]
        if(diff % stepsize > 0):
            raise Exception("Steps dont fit into interval")
        steps = int(diff / stepsize)

        values = []
        for step in xrange(steps):
            value = interval[0] + step * stepsize
            values.append(value)

        self.results = {}

        run = lambda val : self._run_value(val, parameter, args, algorithm)
        if(parallel):
            task = values
            cpus = cpu_count()
            tl = int(float(len(values)) / float(cpus))
            carryover = len(values) % cpus

            task_slices = [task[i * tl : (i+1) * tl] for i in range(0, cpus)]
            if(carryover > 0):
                task_slices.append(task[cpus * tl:])

            sequential = lambda lis : map(run, lis)

            results = pmap(sequential, task_slices)
        else:
            results = map(run, values)

        aggregated = sum(results, [])
        self.results = dict(aggregated)

        tus = [(val, error) for val, error in self.results.iteritems()]
        sortedtus = sorted(tus, key = lambda t : t[1])
        best_val, best_error = sortedtus[0]

        return best_val, best_error

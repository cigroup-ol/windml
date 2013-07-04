from numpy.random import normal, rand

class OnePlusOneEA(object):
#    def __init__():

    def minimize(self, parameter, mean, sigma, interval, iterations, args, algorithm):
        """
        A (1+1)-EA for real parameter optimization of an algorithm. Does
        not adapt step size, the choice of sigma is therefore very important.
    
        parameter: the name of the real parameter to minimize
        mean: mean of population and start position respectively
        sigma: step size of the evolution process
        interval: feasible interval of parameter solutions
        iterations: how many iteration until termination
        args: hashmap of the arguments of algorithm
        algorithm: the algorithm function to optimize, the function
        needs to accept the args hashmap.
    
        Example: Optimizing a custom algorithm
        --------------------------------------------
    
        def algorithm(args):
            # here return the error to minimize
            return args['radius'] ** 2
    
        args = {'otherarg' : 1}
        inte = [0, 10]
        optradius, error = minimize11ea('radius', 1.0, 5.0, inte, 50, args, algorithm)
        """
    
        feasible = False
        while(not feasible):
            parent = normal(mean, sigma)
            if(interval[0] <= parent <= interval[1]):
                print parent
                feasible = True

        args[parameter] = parent
        best_error = algorithm(args)
    
        for i in xrange(iterations):
            feasible = False
            while(not feasible):
                offspring = parent + normal(mean, sigma)
                if(interval[0] <= offspring <= interval[1]):
                    print offspring
                    feasible = True
            args[parameter] = offspring
            error = algorithm(args)
            if(error < best_error):
                parent = offspring
                best_error = error
                print parent, error
    
        return parent, best_error


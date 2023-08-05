import numpy as np
from kneed import DataGenerator, KneeLocator
import math
import numpy as np
import pandas as pd
import scipy.optimize as optim
import matplotlib.pyplot as plt

class entropyHeuristicBinning():

    """ notes
    """

    def __init__(self,signal):
        """Constructor
        Args:
            f (function): function for optimization
            df (function): first derivation of the function
            x_t (float): starting variable for analysis
            learning_rate (float, optional): learning rate
            tolerance (int, optional): tolerance for the distance between two
            consecutive estimates in a subsequence that converges
            max_iterations (int, optional): maximum number of iterations
            n_history_points (int, optional): total amount of history points
            to be saved during optization
        Returns:
            None
        """
        self.signal = signal

    def heuristicbinning(signal):


        def entrp(probs):
            # quantifies the average amount of surprise
            p = np.full(probs.shape, 0.0)
            np.log(probs, out=p, where=(probs > 0))
            return -((p * probs).sum())

        type_sig = type(signal)

        if str(type_sig) == "<class 'numpy.ndarray'>":
            print('ok input datatype')
        if str(type_sig) != "<class 'numpy.ndarray'>":
            print('input cast to numpy.ndarray')
            signal = np.array(signal)


        collate = []
        x = []
        u, c = np.unique(signal, return_counts=True)
        u_   = len(u)

        for l in range(u_):
            hist = np.histogram(signal, bins=l+1, density=True)
            data = hist[0]
            unique, counts = np.unique(data, return_counts=True)
            prob = counts/counts.sum()
            ent = entrp(prob)
            collate.append(ent)
            x.append(l+1)

        print(collate)

        plt.plot(collate)


        # Define funcion with the coefficients to estimate
        def my_logistic(t, a, b, c):
            return 0.0001 + c / (1 + a * np.exp(-b*t))

        # Randomly initialize the coefficients
        p0 = np.random.exponential(size=3)
        p0

        # Set min bound 0 on all coefficients, and set different max bounds for each coefficient
        bounds = (0, [100000., 3., 1000000000.])

        (a,b,c),cov = optim.curve_fit(my_logistic, x, collate, bounds=bounds, p0=p0)

        # Show the coefficients
        a,b,c

        x = np.array(x)
        x

        # Redefine the function with the new a, b and c
        def my_logistic(t):
            return 0.0001 + c / (1 + a * np.exp(-b*t))

        plt.scatter(x, collate)
        plt.plot(x, my_logistic(x))
        plt.title('Logistic Model vs Real Observations')
        plt.legend([ 'Real data', 'Logistic model'])
        plt.xlabel('Bins')
        plt.ylabel('Entropy')


        kneedle = KneeLocator(x, my_logistic(x), S=1.0, curve="concave", direction="increasing")

        print(round(kneedle.knee, 3))

        return round(kneedle.knee, 3),x,collate,my_logistic(x)


import math
import matplotlib.pyplot as plt
import numpy as np
from .GeneralDistribution import Distribution  # (.) for Relative Import
# (for details) https://www.geeksforgeeks.org/absolute-and-relative-imports-in-python/


class Binomial(Distribution):
    def __init__(self, prob=.5, trials=20):
        """ Binomial distribution class for calculating and
            visualizing a Binomial distribution.

            Attributes:
                :param prob (float) representing the probability of an event occurring
                :param trials (int) number of trials

            """

        self.n = trials
        self.p = prob
        self._set_mean()
        self._set_stdev()
        data = np.random.binomial(1, self.p, self.n)
        Distribution.__init__(self, self.mean, self.stdev, data)

    def _calculate_mean(self):

        """Function to calculate the p and n then call _set_mean function.
           Called after reading data from file only.

        Args:
            None

        Returns:
            None

        """

        self.n = len(self.data)
        self.p = sum(self.data) / len(self.data)
        self._set_mean()
    
    def _set_mean(self):
        """Function to calculate the mean from p and n  

                Args:
                    None

                Returns:
                    None

                """
        self.mean = self.p * self.n

    def _calculate_stdev(self):

        """Function to calculate the p and n then call _set_stdev function.
        Called after reading data from file only.

        Args:
            None

        Returns:
            None

        """

        self.n = len(self.data)
        self.p = sum(self.data) / len(self.data)
        self._set_stdev()
        
    def _set_stdev(self):
        """Function to calculate the standard deviation from p and n.

                Args:
                    None

                Returns:
                    None

                """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))

    def plot_bar(self):
        """Function to output a bar plot of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """

        plt.bar(x=['0', '1'], height=[(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')
        plt.show()

    def pmf(self, k):
        """Probability mass function calculator for the Binomial distribution.

        Args:
            k (float): point for calculating the probability mass function


        Returns:
            float: probability mass function output
        """

        return math.factorial(self.n) / (math.factorial(k) * (math.factorial(self.n - k))) \
               * (self.p ** k) * (1 - self.p) ** (self.n - k)

    def plot_bar_pmf(self):

        """Function to plot the pmf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pmf plot
            list: y values for the pmf plot

        """

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pmf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y

    def __add__(self, other):

        """Function to add two Binomial distributions together with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        assert self.p == other.p, 'p values are not equal'

        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.data = np.concatenate([self.data, other.data])
        result._set_mean()
        result._set_stdev()

        return result

    def __repr__(self):

        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial

        """

        return "mean {:.2f}, standard deviation {:.2f}, p {}, n {}". \
            format(self.mean, self.stdev, self.p, self.n)
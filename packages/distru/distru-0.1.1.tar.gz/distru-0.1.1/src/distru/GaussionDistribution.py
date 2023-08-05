import math
import matplotlib.pyplot as plt
import numpy as np
from .GeneralDistribution import Distribution  # (.) for Relative Import
# (for details) https://www.geeksforgeeks.org/absolute-and-relative-imports-in-python/


class Gaussian(Distribution):
    def __init__(self, mu: float = 0, sigma: float = 1, count: int = 100):
        """ Gaussian distribution class for calculating and
                     visualizing a Gaussian distribution.

                  Attributes:
                  :param mu (float) representing the mean value of the distribution
                  :param sigma (float) representing the standard deviation of the distribution
                  :param count (int) a count of the data that will generate randomly at the beginning

           """
        data = np.random.normal(mu, sigma, count)

        Distribution.__init__(self, mu, sigma, data)

    def _calculate_mean(self) -> float:
        """Function to calculate the mean of the data set.

        Args:
            None

        Returns:
            float: mean of the data set

        """

        self.mean = sum(self.data) / len(self.data)

        return self.mean

    def _calculate_stdev(self, sample: bool = True) -> float:

        """Function to calculate the standard deviation of the data set.

        Args:
            sample (bool): whether the data represents a sample or population

        Returns:
            float: standard deviation of the data set

        """

        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)

        sigma = 0

        for d in self.data:
            sigma += (d - self.mean) ** 2

        self.stdev = math.sqrt(sigma / n)

        return self.stdev

    def plot_histogram(self) -> None:
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        plt.hist(self.data)
        plt.title('Histogram of Data')
        plt.xlabel('data')
        plt.ylabel('count')
        plt.show()

    def pdf(self, x: float) -> float:
        """Probability density function calculator for the gaussian distribution.

        Args:
            x (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

        return (1.0 / (self.stdev * math.sqrt(2 * math.pi))) * \
               math.exp(-0.5 * ((x - self.mean) / self.stdev) ** 2)

    def plot_histogram_pdf(self, n_spaces: int = 50):

        """Function to plot the normalized histogram of the data and a plot of the
        probability density function along the same range

        Args:
            n_spaces (int): number of data points

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        min_range = min(self.data)
        max_range = max(self.data)

        # calculates the interval between x values
        interval = (max_range - min_range) / n_spaces

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval * i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[1].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):

        """Function to add two Gaussian distributions together

        Args:
            other (Gaussian): Gaussian instance

        Returns:
            Gaussian: Gaussian distribution

        """

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
        result.data = self.data + other.data

        return result

    def __repr__(self):

        """Function to output the characteristics of the Gaussian instance

        Args:
            None

        Returns:
            string: characteristics of the Gaussian

        """

        return "mean {:.2f}, standard deviation {:.2f}".format(self.mean, self.stdev)
import numpy as np


class Distribution:
    def __init__(self, mean: float, stdev: float, data: np.ndarray) -> None:
        """
        General Distribution class is the parent class for any distribution
        and contain the general attributes and methods.

        Attributes:
        :param mean (float) representing the mean value of the distribution
        :param stdev (float) representing the standard deviation of the distribution
        :param data (numpy array of floats) a list of floats extracted from the data file or generated randomly
        """


        self.mean = mean
        self.stdev = stdev
        self.data = data

    def read_data_file(self, file_name) -> None:
        """Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
            file_name (string): name of a file to read from

        Returns:
            None

        """

        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(float(line))
                line = file.readline()
        file.close()

        self.data = np.array(data_list)

        self._calculate_mean()
        self._calculate_stdev()

    def _calculate_mean(self):
        pass

    def _calculate_stdev(self):
        pass
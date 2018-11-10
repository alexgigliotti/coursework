# -------------------------------------------------------------------------------------------------------------------- #
# Bootstrap Tool
# Alex Gigliotti - UT Austin, BS Petroleum Engineering, May 2019
# GitHub:
# 10/28/2018
#
# This program was created to calculate the uncertainty in sample data using bootstrap. Specifically, it contains a
# series of functions that lead to calculating the uncertainty in the original oil in place (OOIP) using bootstrapped
# porosity and thickness data.
#
# I wrote this program with many small functions for easy debugging and so it could be reused for different scenarios.
# There is also an example calculation shown below the program.
# -------------------------------------------------------------------------------------------------------------------- #

import numpy as np
import matplotlib.pyplot as plt
import pandas


class Bootstrap():

    def __init__(self, filename="sample"):
        # If no filename given, use sample data. Otherwise import data from the csv file and organize it
        if filename == "sample":
            data_count = np.arange(1, 21, 1)
            x1 = np.random.rand(20)
            x2 = np.random.rand(20)
            raw_data = np.array([data_count, x1, x2])
            print(raw_data)
        else:
            raw_data = np.genfromtxt(filename, skip_header=1, delimiter=',')

        self.raw_data = raw_data
        self.x1 = self.raw_data[:, 1]
        self.x2 = self.raw_data[:, 2]
        self.len_data = len(raw_data)

        # Set reservoir constants
        self.area = 1000000  # m^3
        self.ntg = 0.3  # %
        self.So = 1  # %
        self.conversion_factor = 6.26  # bbl/m^3

    def bootstrap(self, data, n_realizations):
        '''
        This function carries out the resampling procedure for bootstrapping

        Inputs:
        data = data to be bootstrapped
        n_realizations = number of realizations for bootstrap

        Return:
        bootstrap_data = array with rows of random resamples and columns of realizations
        resamples = array of random values used to index the data for random sampling
        '''

        n_data = self.len_data

        # Sort the data to set up CDF
        sort_data = np.sort(data)
        sort_data = sort_data[::-1]

        # Bootstrap using given number of realizations.
        resamples = np.random.randint(0, n_data, [n_realizations, n_data])
        bootstrap_data = sort_data[resamples]

        return bootstrap_data, resamples

    def ooip_monte_carlo(self, porosity_realizations, thickness_realizations, n_monte_carlo):
        '''
        Run a Monte Carlo simulation using the bootstrapped porosity and thickness data

        Inputs:
        porosity_realizations = realizations of the mean of porosity
        thickness_realizations = realizations of the mean of thickness
        n_monte_carlo = number of Monte Carlo simulations to run

        Return:
        ooip = the original oil in place
        '''

        # Get the mean and standard deviation of porosity and thickness
        porosity_mean = np.average(porosity_realizations)
        porosity_standard_deviation = self.compute_sample_standard_deviation(porosity_realizations)
        thickness_mean = np.average(thickness_realizations)
        thickness_standard_deviation = self.compute_sample_standard_deviation(thickness_realizations)

        # Use the thickness and porosity distributions (assumed Gaussian due to the Central Limit Theorem) to find OOIP realizations
        porosity_distribution = np.random.normal(porosity_mean, porosity_standard_deviation, n_monte_carlo)
        thickness_distribution = np.random.normal(thickness_mean, thickness_standard_deviation, n_monte_carlo)

        ooip = porosity_distribution * thickness_distribution * self.ntg * self.area * self.So * self.conversion_factor

        return ooip

    def compute_summary_realizations(self, data):
        '''
        Compute summary statistics of the realizations from the output of bootstrap().
        '''

        average = np.average(data, axis=1)
        standard_deviation = np.std(data, axis=1)
        minimum = np.min(data, axis=1)
        maximum = np.max(data, axis=1)

        data_sort = np.sort(data)
        P10 = np.percentile(data_sort, 10)
        P50 = np.percentile(data_sort, 50)
        P90 = np.percentile(data_sort, 90)

        return average, standard_deviation, minimum, maximum, P10, P50, P90

    def compute_sample_standard_deviation(self, data):
        '''
        Calculate the sample standard deviation (degrees of freedom = n-1)
        '''

        sample_standard_deviation = np.std(data, ddof=1)  # setting ddof=1 will use n-1 degrees of freedom

        return sample_standard_deviation

    def compute_standard_error(self, data):
        '''
        Calculate the standard error
        '''

        sample_standard_deviation = self.compute_sample_standard_deviation(data)
        n = len(data)
        standard_error = sample_standard_deviation / np.sqrt(n)

        return standard_error

    def compute_percentiles(self, data):
        '''
        Find the P10, P50, and P90 values of the input data
        '''

        data_sort = np.sort(data)

        P10 = np.percentile(data_sort, 10)
        P50 = np.percentile(data_sort, 50)
        P90 = np.percentile(data_sort, 90)

        return P10, P50, P90

    def plot_cdf(self, data):
        '''
        Create a plot of the CDF of the input data
        '''

        # Create CDF using uniform probability and sorted data
        data_sort = np.sort(data)
        data_cdf = np.linspace(0, 1, len(data))

        # Plot CDF results
        plt.figure()
        plt.plot(data_sort, data_cdf, 'o')

    def run_bootstrap_program(self, n, x1_name="x1"):
        '''
        Runs full bootstrap program with general variable names

        Inputs:
        n = number of realizations
        x1_name = name of variable 1

        Return:
        bootstrap_mean = array of bootstrap mean realizations for x1

        '''

        # Data bootstrap
        x1 = self.x1
        x1_bootstrap = self.bootstrap(x1, n)[0]

        # Compute summary statistics
        bootstrap_mean = self.compute_realization_average(x1_bootstrap)

        # Compute summary statistics percentiles
        standard_deviation_p10, standard_deviation_p50, standard_deviation_p90 = self.compute_percentiles(x1_bootstrap_standard_deviation)

        # Print data tables with Pandas
        realization_n = ["Realization " + str(i + 1) for i in range(n)]
        n_show = 10
        print("\n", pandas.DataFrame(bootstrap_mean[0:n_show], realization_n[0:n_show], [str("Average " + x1_name)]))

        # Calculate bootstrap standard deviation and standard error of sample data for verification
        x1_bootstrap_standard_deviation = bootstrap.compute_sample_standard_deviation(bootstrap_mean)
        x1_sample_standard_error = bootstrap.compute_standard_error(x1)
        print("Bootstrap Verification", "\n")
        print(pandas.DataFrame([[x1_bootstrap_standard_deviation], [x1_sample_standard_error]], ["Bootstrap Standard Deviation", "Sample Standard Error"], [x1_name]))





        return bootstrap_mean,


'''
Example calculation
'''

bootstrap = Bootstrap()  # 'Por_Thick_Small.csv'

# number of realizations to complete
n = 100

porosity_bootstrap_mean, thickness_bootstrap_mean = bootstrap.run_bootstrap_program(n, "x1", "x2")

# Calculate OOIP from bootstrap data
ooip_from_bootstrap = bootstrap.ooip_monte_carlo(porosity_bootstrap_mean, thickness_bootstrap_mean, n)

# Calculate bootstrap OOIP percentiles
percentiles = bootstrap.compute_percentiles(ooip_from_bootstrap)
print(pandas.DataFrame([percentiles[0], percentiles[1], percentiles[2]], ["P10", "P50", "P90"],
                       ["OOIP Percentile Value"]))

# Plot OOIP Monte Carlo CDF
bootstrap.plot_cdf(ooip_from_bootstrap)
plt.xlabel('bbl oil')
plt.ylabel('Cumulative Probability')
plt.yticks(np.arange(0, 1.1, step=0.1))
plt.title('CDF of OOIP Monte Carlo Using Bootstrapped Data')
plt.grid()
plt.show()


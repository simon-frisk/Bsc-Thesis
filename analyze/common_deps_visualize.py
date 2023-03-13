import matplotlib.pyplot as plt


def histogram(dependency_dictionary):
    """
    Takes a dictionary with dependency names as keys, and list of root packages using this dependency as value,
    and plots histogram of frequency of usage for the different dependencies.
    """
    # List, where for each dependency, we will put an int of how many times it is used by a root package
    dependency_usage = []

    # Loop through all dependencies and add usage frequency to above list
    for dependency in dependency_dictionary:
        usage_count = len(dependency_dictionary[dependency])
        dependency_usage.append(usage_count)

    num_bins = max(dependency_usage) - min(dependency_usage)
    plt.hist(dependency_usage, bins=num_bins)
    plt.yscale("log")
    plt.ylabel("Number of dependencies")
    plt.xlabel("Number of times used by root package")
    plt.show()

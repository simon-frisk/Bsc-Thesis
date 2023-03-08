import dependency_metrics
import matplotlib.pyplot as plt


def latest_version_tree_sizes(dataset):
    sizes = []

    for package in dataset.values():
        version = package[-1]
        size = dependency_metrics.tree_size(version)
        sizes.append(size)
    return sizes


def all_tree_sizes(dataset):
    sizes = []

    for package in dataset.values():
        for version in package:
            size = dependency_metrics.tree_size(version)
            sizes.append([size, version.name])
            #sizes.append(size)
    sizes.sort()
    return sizes


def all_tree_level1_sizes(dataset):
    sizes = []

    for package in dataset.values():
        for version in package:
            size = dependency_metrics.num_layer1_deps(version)
            sizes.append(size)
    return sizes


def size_histogram(dataset):
    sizes = all_tree_sizes(dataset)
    bin_width = 100
    plt.hist(sizes, bins=range(min(sizes), max(sizes) + bin_width, bin_width))
    plt.title("Size distribution of trees")
    plt.ylabel("Number of trees")
    plt.xlabel("Tree size, No. Dependencies")
    plt.yscale('log')
    plt.grid()
    plt.show()


def layer_1_histogram(dataset):
    data = all_tree_level1_sizes(dataset)
    bin_width = 1
    plt.hist(data, bins=range(min(data), max(data) + bin_width, bin_width))
    plt.title("Distribution of first layer dependencies")
    plt.ylabel("Number of trees")
    plt.xlabel("No. Dependencies")
    plt.grid()
    plt.show()
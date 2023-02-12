import dependency_metrics
import matplotlib.pyplot as plt


def latest_version_tree_sizes(dataset):
    sizes = []

    for package in dataset.values():
        version = package[-1]
        size = dependency_metrics.tree_size(version)
        sizes.append(size)
    return sizes


def size_histograms(dataset):
    sizes = latest_version_tree_sizes(dataset)
    print(len(sizes))
    plt.hist(sizes, bins=50)
    plt.title("Size distribution of tree of latest version in all packages")
    plt.ylabel("Number of trees")
    plt.xlabel("Tree size, No. Dependencies")
    plt.yscale('log')
    plt.show()
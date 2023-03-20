import matplotlib.pyplot as plt
import violin_plots


def existence_timeline(package, offset):
        num_versions = len(package)
        X = [i/(num_versions - 1) for i in range(num_versions)]
        number_of_dependencies = []
        max = 0
        min = 10000000
        for version in package:
            unique_deps = []
            violin_plots._number_of_deps(version, unique_deps)
            size = len(unique_deps)-1
            number_of_dependencies.append(size)
            if size > max: max = size
            if size < min: min = size
        for i in range(len(number_of_dependencies)):
            number_of_dependencies[i] = (number_of_dependencies[i] - min)/max + offset
        return X, number_of_dependencies

def timeline_plot(dataset):
    for i, package in enumerate(dataset.values()):
        y, x = existence_timeline(package, i)

        plt.plot(x, y)
    plt.show()




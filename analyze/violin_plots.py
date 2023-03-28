import matplotlib.pyplot as plt

def number_of_versions_loaded(dataset):
    num_versions_list = []
    for package in dataset.values():
        num_versions_list.append(len(package))

    return num_versions_list

def first_version_dependencies(dataset):
    first_version_deps_list = []
    for package in dataset.values():
        deps_list = []
        _number_of_deps(package[0], deps_list)
        first_version_deps_list.append(len(deps_list)-1)
    return first_version_deps_list

def last_version_dependencies(dataset):
    last_version_deps_list = []
    for package in dataset.values():
        deps_list = []
        _number_of_deps(package[-1], deps_list)
        last_version_deps_list.append(len(deps_list) - 1)
    return last_version_deps_list

def _number_of_deps(node, list):
    if node.name not in list:
        list.append(node.name)

    if node.dependencies != []:
        for dependency in node.dependencies:
            _number_of_deps(dependency, list)

def lines_of_code():
    return

def violin_plots(dataset):
    num_versions = number_of_versions_loaded(dataset)
    first_version_deps = first_version_dependencies(dataset)
    last_version_deps = last_version_dependencies(dataset)
    #print(first_version_deps)
    plt.violinplot([num_versions, first_version_deps, last_version_deps], showmedians=True, quantiles=[[0.25, 0.5, 0.75], [0.25, 0.5, 0.75],[0.25, 0.5, 0.75]])
    plt.yscale("log")
    plt.show()
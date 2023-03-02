
def dependency_dictionary(dataset):
    dep_dict = {}

    for package in dataset.values():
        print('package')
        for version in package:
            _dict_add(version, dep_dict, version.name)

    return dep_dict

def _dict_add(node, dict, package_name):
    if node.name in dict.keys():
        if package_name not in dict[node.name]:
            dict[node.name].append(package_name)
    else:
        dict[node.name] = [package_name]

    if node.dependencies != []:
        for dependency in node.dependencies:
            _dict_add(dependency, dict, package_name)

def dep_dict_stats(dataset):
    dep_dict = dependency_dictionary(dataset)
    number_of_packages = []
    for key in dep_dict.keys():
        number_of_packages.append([len(dep_dict[key]), key])

    number_of_packages.sort()

    return number_of_packages[-10:], len(number_of_packages)


def total_number_of_deps(dataset):
    list_of_unique_dependencies = []
    for package in dataset.values():
        for version in package:
            _dfs_name_search(version, list_of_unique_dependencies)

    print(len(list_of_unique_dependencies))  #2008 unique dependencies (including 100 packages)
    return(list_of_unique_dependencies)

def _dfs_name_search(node, list):
    if node.name not in list:
        list.append(node.name)
    if node.dependencies != []:
        for dependency in node.dependencies:
            _dfs_name_search(dependency, list)




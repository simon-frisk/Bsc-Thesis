
def dependency_dictionary(dataset):
    '''Creates a dictionary of all the different dependencies in the dataset where every
    dependency contains a list of the packages where this dependency is called'''
    dep_dict = {}

    for package in dataset.values():
        print('package')
        for version in package:
            _dict_add(version, dep_dict, version.name)

    return dep_dict

def _dict_add(node, dict, package_name):
    '''Help function for generating dependency dictionary'''
    if node.name in dict.keys():
        if package_name not in dict[node.name]:
            dict[node.name].append(package_name)
    else:
        dict[node.name] = [package_name]

    if node.dependencies != []:
        for dependency in node.dependencies:
            _dict_add(dependency, dict, package_name)

def dep_dict_stats(dataset):
    '''returns information on dependencies'''
    dep_dict = dependency_dictionary(dataset)
    number_of_packages = []
    for key in dep_dict.keys():
        number_of_packages.append([len(dep_dict[key]), key])

    number_of_packages.sort()

    return number_of_packages[-10:], len(number_of_packages) #10 most used dependencies, total number of dependencies in entire dataset


def total_number_of_deps(dataset):
    '''Returns list of all dependencies in dataset'''
    list_of_unique_dependencies = []
    for package in dataset.values():
        for version in package:
            _dfs_name_search(version, list_of_unique_dependencies)

    print(len(list_of_unique_dependencies))  #2008 unique dependencies (including 100 packages)
    return(list_of_unique_dependencies)

def _dfs_name_search(node, list):
    '''Help function for deps list above'''
    if node.name not in list:
        list.append(node.name)
    if node.dependencies != []:
        for dependency in node.dependencies:
            _dfs_name_search(dependency, list)


def print_tree(dataset):
    dep_list = []
    dep_list_copy = []
    for package in dataset.values():
        if package[0].name == 'ember-cli-babel':
            for version in package:
                if version.version == '7.26.11':
                    _print_tree_help(version, dep_list_copy, 0)
                    dep_list_copy.append(version.version)
                '''if len(dep_list) > len(dep_list_copy):
                    dep_list_copy = dep_list.copy()
                    dep_list = []'''


    #dep_list_copy.sort()
    print(dep_list_copy)
    print(len(dep_list_copy))
    return

def _print_tree_help(node, list, depth):
    list.append([node.name, depth])
    if node.dependencies != []:
        for dependency in node.dependencies:
            _print_tree_help(dependency, list, depth+1)
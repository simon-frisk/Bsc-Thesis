

def dependency_dictionary(dataset, latest=0):
    '''Creates a dictionary of all the different dependencies in the dataset where every
    dependency contains a list of the packages where this dependency is called'''
    dep_dict = {}

    for package in dataset.values():
        if latest == 0:
            for version in package:
                _dict_add(version, dep_dict, version.name)
        else:
            _dict_add(package[-1], dep_dict, package[-1].name) #Most recent version of packages

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


def dep_dict_stats(dataset, latest=0):
    '''returns information on dependencies'''
    dep_dict = dependency_dictionary(dataset, latest)
    number_of_packages = []
    for key in dep_dict.keys():
        number_of_packages.append([len(dep_dict[key]), key])

    number_of_packages.sort()

    return number_of_packages[-10:] #10 most used dependencies

def dependency_dictionary_with_versions(dataset, latest=0):
    dep_dict = {}
    for package in dataset.values():
        if latest==0:
            for version in package:
                _dict_add_versions(version, dep_dict, version.name, version.version, depth=0)
        else:
            _dict_add_versions(package[-1], dep_dict, package[-1].name, package[-1].version, depth=0)
    return dep_dict

def _dict_add_versions(node, dictionary, package_name, package_version, depth):
    if node.name in dictionary.keys():
        if package_name in dictionary[node.name].keys():
            if package_version in dictionary[node.name][package_name].keys():
                if dictionary[node.name][package_name][package_version] > depth:
                    dictionary[node.name][package_name][package_version] = depth
            else:
                dictionary[node.name][package_name][package_version] = depth

        else:
            dictionary[node.name][package_name] = {package_version:depth}
    else:
        dictionary[node.name] = {package_name:{package_version:depth}}

    if node.dependencies != []:
        for dependency in node.dependencies:
            _dict_add_versions(dependency, dictionary, package_name, package_version, depth+1)

def dep_dict_stats_versions(dataset, simplify=0):
    dict = dependency_dictionary_with_versions(dataset)
    most_popular_list = []
    for info in dep_dict_stats(dataset):
        key = info[1]
        most_popular_list.append(key)

    most_popular_dict = {key: dict[key] for key in most_popular_list}

    if simplify == 1:
        for unique_dependency in most_popular_dict.keys():
            for unique_package in most_popular_dict[unique_dependency].keys():
                #total_number_of_versions = #Want to find what percentage of major/minor/patch bump versions the dependency appears in
                most_popular_dict[unique_dependency][unique_package] = len(most_popular_dict[unique_dependency][unique_package].keys())

    return most_popular_dict



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

    for package in dataset.values():
        if package[0].name == 'handlebars':
            for version in package:
                if version.version == '4.7.7':
                    dep_list_copy = []
                    _print_tree_help(version, dep_list_copy, 0)
                    version.print()
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
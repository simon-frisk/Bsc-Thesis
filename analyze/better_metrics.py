import find_common_deps
import size_compare


def depth_of_common_dependencies(dataset):
    '''Returns a dictionary with all unique dependencies as keys, and a list of the average depth
    per package in which they appear as values'''
    dependency_dictionary = find_common_deps.dependency_dictionary_with_versions(dataset)
    depth_dictionary = {}
    for unique_dependency in dependency_dictionary.keys():
        average_depths_in_package = []
        for unique_package in dependency_dictionary[unique_dependency].keys():
            depths_in_versions = []
            for unique_version in dependency_dictionary[unique_dependency][unique_package].keys():
                if dependency_dictionary[unique_dependency][unique_package][unique_version] != 0:
                    depths_in_versions.append(dependency_dictionary[unique_dependency][unique_package][unique_version])
            if depths_in_versions == []:
                continue
            average_depths_in_package.append(sum(depths_in_versions)/len(depths_in_versions))
        depth_dictionary[unique_dependency] = average_depths_in_package

    print(dependency_dictionary["minimist"])
    print(dependency_dictionary["mkdirp"])
    return depth_dictionary





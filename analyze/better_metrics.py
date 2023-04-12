import find_common_deps
import size_compare
import common_deps_parents

def depth_of_common_dependencies(dataset, latest):
    '''Returns a dictionary with all unique dependencies as keys, and a list of the average depth
    per package in which they appear as values'''
    dependency_dictionary = find_common_deps.dependency_dictionary_with_versions(dataset, latest)
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
        if average_depths_in_package != []:
            average_depths_in_package.append([sum(average_depths_in_package)/len(average_depths_in_package)])
        depth_dictionary[unique_dependency] = average_depths_in_package

    #print(dependency_dictionary["minimist"])
    #print(dependency_dictionary["mkdirp"])
    return depth_dictionary

def stats_for_most_common_deps(dataset):
    list_of_most_common_deps = find_common_deps.dep_dict_stats(dataset, 1)
    depth_dictionary = depth_of_common_dependencies(dataset, 1)
    common_deps_with_stats_list = []
    common_deps_name_list = []
    for dependency in list_of_most_common_deps:
        key = dependency[1]
        number_first_layer = 0
        total = 0
        for depth in depth_dictionary[key]:
            if depth == 1:
                number_first_layer +=1
            total+=1
        common_deps_name_list.append(key)
        common_deps_with_stats_list.append([key, number_first_layer/total, depth_dictionary[key]])

    common_deps_parents.common_deps_parents(dataset, common_deps_name_list)
    return(common_deps_with_stats_list)


def first_layer_at_any_point(dataset):
    return







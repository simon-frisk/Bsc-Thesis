import dependency_tree.serialize as serialize
import dependency_metrics
import data_util
import os
import analyze_changes
import size_visualize
import find_common_deps
import common_deps_visualize
import better_metrics
import common_deps_parents

serialized_dir = '../serialized/2023-02-12'


def load_data_set():
    """
    Helper function for loading whole dataset. Load into a dictionary with key package name,
    and value is a list of dependency_node objects, one for each version
    """
    data_set = {}
    package_dicts = os.listdir(serialized_dir)
    excluded = 0
    for package_name in package_dicts:
        package = []
        package_dir = os.path.join(serialized_dir, package_name)
        files = os.listdir(package_dir)
        files.sort()
        for file_name in files:
            dep_tree = serialize.load(os.path.join(package_dir, file_name))
            package.append(dep_tree)
        # Don't include packages where no version has a dependency
        has_dependency = False
        for version in package:
            if len(version.dependencies) != 0:
                has_dependency = True
        if not has_dependency:
            excluded += 1
            continue
        # Add to dataset
        data_set[package_name] = package
    print(f"Excluded {excluded} packages, because they had no dependencies")
    return data_set


if __name__ == '__main__':
    print("Starting analysis")
    print("Loading dataset ...")
    dataset = load_data_set()
    print("Finished loading dataset:", len(dataset), "packages")
    # Metrics about the trees
    #analyze_changes.print_avg_layer_1_deps(dataset)
    #analyze_changes.print_avg_depth_and_num_deps(dataset)
    #size_visualize.size_histogram(dataset)
    #size_visualize.layer_1_histogram(dataset)
    # Metrics about bumps
    #analyze_changes.print_avg_change_patches(dataset)
    #analyze_changes.analyze_new_dependencies(dataset)
    #analyze_changes.analyze_changes_add_subtract(dataset)
    #analyze_changes.histogram_changes(dataset)
    #x = find_common_deps.dependency_dictionary(dataset)
    #common_deps_visualize.histogram(x)
    x = find_common_deps.dependency_dictionary(dataset)
    common_deps_parents.common_deps_parents(dataset, ["minimist"])
    #common_deps_visualize.histogram(x)
    #print(find_common_deps.dependency_dictionary_with_versions(dataset))
    #print(find_common_deps.dep_dict_stats(dataset))
    #print(find_common_deps.total_number_of_deps(dataset))
    #print(find_common_deps.print_tree(dataset))
    #find_common_deps.print_dict(dataset)
    #print(size_visualize.all_tree_sizes(dataset))
    #size_compare.size_list(dataset)
    print(better_metrics.depth_of_common_dependencies(dataset))

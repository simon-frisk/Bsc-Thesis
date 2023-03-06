import dependency_tree.serialize as serialize
import dependency_metrics
import data_util
import os
import analyze_changes
import size_visualize
import find_common_deps
import size_compare

serialized_dir = '../serialized/2023-02-12'


def get_package(package):
    versions =[]
    directory_path = os.path.join(serialized_dir, package)
    files = os.listdir(directory_path)
    for file_name in files:
        dep_tree = serialize.load(os.path.join(directory_path, file_name))
        versions.append(dep_tree)
    data_util.sort_tree_list(versions)
    return versions


def load_data_set():
    data_set = {}
    package_dicts = os.listdir(serialized_dir)
    for package_name in package_dicts:
        package = []
        package_dir = os.path.join(serialized_dir, package_name)
        files = os.listdir(package_dir)
        files.sort()
        for file_name in files:
            dep_tree = serialize.load(os.path.join(package_dir, file_name))
            package.append(dep_tree)
        data_set[package_name] = package
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
    print(find_common_deps.dep_dict_stats(dataset))
    #print(find_common_deps.total_number_of_deps(dataset))
    #print(find_common_deps.print_tree(dataset))
    #print(size_visualize.all_tree_sizes(dataset))
    #size_compare.size_list(dataset)

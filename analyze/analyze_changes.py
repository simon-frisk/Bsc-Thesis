import data_util
import dependency_metrics
import numpy as np
import matplotlib.pyplot as plt


def print_avg_depth_and_num_deps(dataset):
    total_num_deps = 0
    total_depth = 0
    num_trees = 0
    for package in dataset.values():
        for version in package:
            stats = dependency_metrics.tree_depth_and_edges(version)
            total_depth += stats[0]
            total_num_deps += stats[1]
            num_trees += 1
    avg_num_deps = total_num_deps / num_trees
    avg_depth = total_depth / num_trees
    print("Average depth and number of dependencies: ", avg_depth, avg_num_deps)


def print_avg_layer_1_deps(dataset):
    total_deps = 0
    num_trees = 0
    for package in dataset.values():
        for version in package:
            total_deps += dependency_metrics.num_layer1_deps(version)
            num_trees += 1
    avg_num_deps = total_deps / num_trees
    print(f"Average number of layer 1 dependencies: {avg_num_deps}")


def histogram_changes(dataset):
    layer_1_changes = [[], [], []]
    num_deps_changes = [[], [], []]

    for package in dataset.values():
        major_bumps = data_util.get_bumps(package, 'major')
        minor_bumps = data_util.get_bumps(package, 'minor')
        patch_bumps = data_util.get_bumps(package, 'patch')

        for (old, new) in major_bumps:
            layer_1_changes[0].append(dependency_metrics.num_layer1_deps(new) - dependency_metrics.num_layer1_deps(old))
            num_deps_changes[0].append(dependency_metrics.tree_size(new) - dependency_metrics.tree_size(old))
        for (old, new) in minor_bumps:
            layer_1_changes[1].append(dependency_metrics.num_layer1_deps(new) - dependency_metrics.num_layer1_deps(old))
            num_deps_changes[1].append(dependency_metrics.tree_size(new) - dependency_metrics.tree_size(old))
        for (old, new) in patch_bumps:
            layer_1_changes[2].append(dependency_metrics.num_layer1_deps(new) - dependency_metrics.num_layer1_deps(old))
            num_deps_changes[2].append(dependency_metrics.tree_size(new) - dependency_metrics.tree_size(old))

    for layer_1_changes, bump_type, bins in zip(layer_1_changes, ["major", "minor", "patch"], [20, 20, 10]):
        plt.hist(layer_1_changes, bins=bins)
        plt.title(bump_type)
        plt.ylabel("Number of trees")
        plt.xlabel("Change in layer 1 dependencies")
        plt.yscale('log')
        plt.grid()
        plt.show()

    for num_deps_changes, bump_type, bins in zip(num_deps_changes, ["major", "minor", "patch"], [20, 100, 100]):
        plt.hist(num_deps_changes, bins=bins)
        plt.title(bump_type)
        plt.ylabel("Number of trees")
        plt.xlabel("Change in num dependencies")
        plt.yscale('log')
        plt.grid()
        plt.show()


def print_avg_change_patches(dataset):
    """Print average change in tree depth, num layer 1 deps and number of dependencies for different bump types."""
    total_num_bumps = np.zeros(3)
    total_depths = [0, 0, 0]
    total_deps = [0, 0, 0]
    total_layer_1 = [0, 0, 0]

    for package in dataset.values():
        major_bumps = data_util.get_bumps(package, 'major')
        minor_bumps = data_util.get_bumps(package, 'minor')
        patch_bumps = data_util.get_bumps(package, 'patch')
        total_num_bumps[0] += len(major_bumps)
        total_num_bumps[1] += len(minor_bumps)
        total_num_bumps[2] += len(patch_bumps)

        for (old, new) in major_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_depths[0] += change[0]
            total_deps[0] += change[1]
            total_layer_1[0] += dependency_metrics.num_layer1_deps(new) - dependency_metrics.num_layer1_deps(old)

        for (old, new) in minor_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_depths[1] += change[0]
            total_deps[1] += change[1]
            total_layer_1[1] += dependency_metrics.num_layer1_deps(new) - dependency_metrics.num_layer1_deps(old)

        for (old, new) in patch_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_depths[2] += change[0]
            total_deps[2] += change[1]
            total_layer_1[2] += dependency_metrics.num_layer1_deps(new) - dependency_metrics.num_layer1_deps(old)

    print("Average changes in depth, num dependencies and layer 1 dependencies")
    print(f"Major Bumps: {total_depths[0]/total_num_bumps[0]}, {total_deps[0]/total_num_bumps[0]}, {total_layer_1[0]/total_num_bumps[0]}")
    print(f"Minor Bumps: {total_depths[1]/total_num_bumps[1]}, {total_deps[1]/total_num_bumps[1]}, {total_layer_1[1]/total_num_bumps[1]}")
    print(f"Patch Bumps: {total_depths[2]/total_num_bumps[2]}, {total_deps[2]/total_num_bumps[2]}, {total_layer_1[2]/total_num_bumps[2]}")


def analyze_changes_add_subtract(dataset):
    total_num_bumps = [0, 0, 0]
    added_deps = [[], [], []]
    subtracted_deps = [[], [], []]


    for package in dataset.values():
        major_bumps = data_util.get_bumps(package, 'major')
        minor_bumps = data_util.get_bumps(package, 'minor')
        patch_bumps = data_util.get_bumps(package, 'patch')
        total_num_bumps[0] += len(major_bumps)
        total_num_bumps[1] += len(minor_bumps)
        total_num_bumps[2] += len(patch_bumps)

        for (old, new) in major_bumps:
            new_added_dependencies = dependency_metrics.find_new_dependencies(old, new)
            new_subtracted_dependencies = dependency_metrics.find_new_dependencies(new, old)
            added_deps[0].append(len(new_added_dependencies))
            subtracted_deps[0].append(len(new_subtracted_dependencies))

    plt.clf()
    plt.hist(added_deps[0], bins=20)
    plt.yscale("log")
    plt.show()





def analyze_changes_where(dataset):
    total_num_bumps = [0, 0, 0]
    total_change = [[0, 0], [0, 0], [0, 0]]
    total_added_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    total_subtracted_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    total_num_bumps_w_new_deps = [[0, 0, 0], [0, 0, 0], [0,0,0]]

    for package in dataset.values():
        major_bumps = data_util.get_bumps(package, 'major')
        minor_bumps = data_util.get_bumps(package, 'minor')
        patch_bumps = data_util.get_bumps(package, 'patch')
        total_num_bumps[0] += len(major_bumps)
        total_num_bumps[1] += len(minor_bumps)
        total_num_bumps[2] += len(patch_bumps)

        for (old, new) in major_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_change[0] = np.add(change, total_change[0])

            new_added_dependencies = dependency_metrics.find_new_dependencies(old, new)
            new_subtracted_dependencies = dependency_metrics.find_new_dependencies(new, old)
            if new_added_dependencies != [] or new_subtracted_dependencies != []:
                total_num_bumps_w_new_deps[0][2] += 1
                if new_added_dependencies != []:
                    total_num_bumps_w_new_deps[0][0]+= 1
                if new_subtracted_dependencies != []:
                    total_num_bumps_w_new_deps[0][1] += 1

                for new_dependency in new_added_dependencies:
                    total_added_stats[0][0] += new_dependency[1]
                    total_added_stats[0][1] += new_dependency[2][0]
                    total_added_stats[0][2] += new_dependency[2][1]
                for new_dependency in new_subtracted_dependencies:
                    total_subtracted_stats[0][0] += new_dependency[1]
                    total_subtracted_stats[0][1] += new_dependency[2][0]
                    total_subtracted_stats[0][2] += new_dependency[2][1]


        for (old, new) in minor_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_change[1] = np.add(change, total_change[1])

            new_added_dependencies = dependency_metrics.find_new_dependencies(old, new)
            new_subtracted_dependencies = dependency_metrics.find_new_dependencies(new, old)
            if new_added_dependencies != [] or new_subtracted_dependencies != []:
                total_num_bumps_w_new_deps[1][2] += 1
                if new_added_dependencies != []:
                    total_num_bumps_w_new_deps[1][0] += 1
                if new_subtracted_dependencies != []:
                    total_num_bumps_w_new_deps[1][1] += 1

                for new_dependency in new_added_dependencies:
                    total_added_stats[1][0] += new_dependency[1]
                    total_added_stats[1][1] += new_dependency[2][0]
                    total_added_stats[1][2] += new_dependency[2][1]
                for new_dependency in new_subtracted_dependencies:
                    total_subtracted_stats[1][0] += new_dependency[1]
                    total_subtracted_stats[1][1] += new_dependency[2][0]
                    total_subtracted_stats[1][2] += new_dependency[2][1]

        for (old, new) in patch_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_change[2] = np.add(change, total_change[2])

            '''new_added_dependencies = dependency_metrics.find_new_dependencies(old, new)
            new_subtracted_dependencies = dependency_metrics.find_new_dependencies(new, old)
            if new_added_dependencies != [] or new_subtracted_dependencies != []:
                total_num_bumps_w_new_deps[2][2] += 1
                if new_added_dependencies != []:
                    total_num_bumps_w_new_deps[2][0] += 1
                if new_subtracted_dependencies != []:
                    total_num_bumps_w_new_deps[2][1] += 1

                added_deps = 0
                average_depth_level = 0
                average_depth_of_dep = 0
                average_edges_of_dep = 0

                for new_dependency in new_added_dependencies:
                    added_deps += 1
                    average_depth_level += new_dependency[1]
                    average_depth_of_dep += new_dependency[2][0]
                    average_edges_of_dep += new_dependency[2][1]

                total_added_stats[2][0] += average_depth_level/added_deps
                total_added_stats[2][1] += average_depth_of_dep/added_deps
                total_added_stats[2][2] += average_edges_of_dep/added_deps

                subbed_deps = 0
                average_depth_level = 0
                average_depth_of_dep = 0
                average_edges_of_dep = 0

                for new_dependency in new_subtracted_dependencies:
                    subbed_deps += 1
                    average_depth_level += new_dependency[1]
                    average_depth_of_dep += new_dependency[2][0]
                    average_edges_of_dep += new_dependency[2][1]

                total_subtracted_stats[2][0] += average_depth_level / subbed_deps
                total_subtracted_stats[2][1] += average_depth_of_dep / subbed_deps
                total_subtracted_stats[2][2] += average_edges_of_dep / subbed_deps'''


    print(total_num_bumps, total_change, total_num_bumps_w_new_deps, total_added_stats, total_subtracted_stats)



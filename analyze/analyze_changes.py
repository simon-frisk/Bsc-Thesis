import data_util
import dependency_metrics
import numpy as np


def analyze_changes(dataset):
    total_num_bumps = np.zeros(3)
    total_change = np.zeros((3, 2))

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

        for (old, new) in minor_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_change[1] = np.add(change, total_change[1])

        for (old, new) in patch_bumps:
            old_stats = dependency_metrics.tree_depth_and_edges(old)
            new_stats = dependency_metrics.tree_depth_and_edges(new)
            change = np.subtract(new_stats, old_stats)
            total_change[2] = np.add(change, total_change[2])

    print(total_num_bumps, total_change)
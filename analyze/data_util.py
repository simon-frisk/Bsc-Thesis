import semantic_version
from functools import cmp_to_key

def get_bumps(tree_list, bump_type):
    '''Return a list of 2-tuples of trees with a version bump of bump_type string(patch, minor, major)'''
    bumps = []
    for i in range(1, len(tree_list)):
        prev_tree = tree_list[i-1]
        current_tree = tree_list[i]
        prev_version = list(map(lambda x: int(x), prev_tree.version.split('.')))
        current_version = list(map(lambda x: int(x), current_tree.version.split('.')))
        if bump_type == 'major' and current_version[0] > prev_version[0]:
            bumps.append((prev_tree, current_tree))
        elif bump_type == 'minor' and current_version[1] > prev_version[1] and current_version[0] == prev_version[0]:
            bumps.append((prev_tree, current_tree))
        elif bump_type == 'patch' and current_version[2] > prev_version[2] and current_version[0] == prev_version[0] and current_version[1] == prev_version[1]:
            bumps.append((prev_tree, current_tree))
    return bumps

def _compare_version_key(v1, v2):
    if (semantic_version.Version(v1.version) > semantic_version.Version(v2.version)) == False:
        return -1
    return 1

def sort_tree_list(tree_list):
    tree_list.sort(key=cmp_to_key(_compare_version_key))
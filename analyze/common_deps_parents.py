from dependency_tree.dependency_node import DependencyNode


def unique_parents(dataset, dependency):
    """
    Count number of unique parents of some dependency in all packages in all versions
    """
    parents_set = set()  # Use a set to keep track of all parents

    for package_versions in dataset.values():
        for version in package_versions:
            _unique_parents_dfs(version, dependency, parents_set)

    return parents_set


def _unique_parents_dfs(tree_node, dependency, parents_set, parent_name=None):
    """
    Return a list of unique parents to dependency in some dependency tree
    """
    if tree_node.name == dependency and parent_name:
        parents_set.add(parent_name)
    for child_node in tree_node.dependencies:
        _unique_parents_dfs(child_node, dependency, parents_set, tree_node.name)


# ---
# The two functions below here find parents in the last version of packages
# ---


def common_deps_parents(dataset, dependencies):
    """
    This function looks at the latest version for every package, and for every dependency in dependencies,
    finds all parents of this dependency and how many times that is the parent.
    """
    # List containing dictionary mapping from parent package name to number of times
    # the dependency has that parent
    dependency_parents = [{} for _ in dependencies]
    # Create a dictionary for fast finding of whether a dependency in dependencies and its index
    dependency_hash = {}
    for i, dep in enumerate(dependencies):
        dependency_hash[dep] = i
    # Iterate through packages
    for package in dataset:
        # Get the latest version dependency tree
        tree = dataset[package][-1]
        # Do a dfs search and update dependency_parents
        _dependency_parent_search(tree, dependency_hash, dependency_parents, tree)
    for dep, parents in zip(dependency_hash, dependency_parents):
        print(f"{dep}: {parents}")


def _dependency_parent_search(node, dependency_hash, dependency_parents, root, parent_node=None, parents_in_tree=None):
    if parent_node is None:
        parents_in_tree = set()
        parent_node = DependencyNode("root", 0, 0)
    if node.name in dependency_hash and parent_node.name not in parents_in_tree:
        parents_in_tree.add(parent_node.name)
        if parent_node.name in dependency_parents[dependency_hash[node.name]]:
            dependency_parents[dependency_hash[node.name]][parent_node.name] += 1
        else:
            dependency_parents[dependency_hash[node.name]][parent_node.name] = 1
    for child in node.dependencies:
        _dependency_parent_search(child, dependency_hash, dependency_parents, root, node, parents_in_tree)

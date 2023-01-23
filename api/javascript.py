import requests
import semantic_version
from dependency_tree.dependency_node import DependencyNode
from dependency_tree.serialize import serialize

NPM_REGISTRY_API_URL = 'https://registry.npmjs.org/{}'


def select_version(semver_spec, versions):
    """Select the matching version from versions list, using semverspec as matching scheme"""

    # TODO: Handle latest and next
    if semver_spec == 'latest' or semver_spec == 'next':
        semver_spec = '*'

    spec = semantic_version.NpmSpec(semver_spec)

    for version in reversed(versions):
        semver = semantic_version.Version(version)
        if semver in spec:
            return version

    raise "No matching version was found"


def fetch_dependency_from_npm_registry(package, parent_semver):
    """Create a dependency graph node for a javascript package"""
    print("Fetching", package, parent_semver, end='... ')

    # Get data from npm registry
    response = requests.get(NPM_REGISTRY_API_URL.format(package))
    if response.status_code != 200:
        raise "Failed to fetch package"
    package = response.json()

    # Select the correct version of the package
    version = select_version(parent_semver, list(package['versions'].keys()))

    version_data = package['versions'][version]

    # Create DependencyNode object
    node = DependencyNode(version_data["name"], version, parent_semver)
    # Find dependencies
    if "dependencies" in version_data:
        dependencies = version_data["dependencies"]
    else:
        dependencies = []

    print("Finished", version)
    # Return a DependencyNode and the dictionary with dependencies
    return node, dependencies


def build_nested_dependencies(parent_node, dependency_dict):
    """Recursive function to fetch and add dependencies to the tree"""
    for dependency in dependency_dict:
        dependency_node, nest_dependencies = fetch_dependency_from_npm_registry(dependency, dependency_dict[dependency])
        parent_node.add_dependency(dependency_node)
        build_nested_dependencies(dependency_node, nest_dependencies)


def build_tree_from_npm_registry(package, version):
    """"
    Create and return dependency tree
    """
    root_node, root_dependencies = fetch_dependency_from_npm_registry(package, version)
    build_nested_dependencies(root_node, root_dependencies)
    return root_node


# Create and save dependency tree for some package
if __name__ == "__main__":
    node = build_tree_from_npm_registry('@tensorflow/tfjs', '0.0.1')
    node.print()
    serialize(node)



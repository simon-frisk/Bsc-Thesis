import requests
import re
import semantic_version
from dependency_tree.dependency_node import DependencyNode
from dependency_tree.serialize import serialize

NPM_REGISTRY_API_URL = 'https://registry.npmjs.org/{}'


def select_version(semver_spec, versions, dist_tags):
    """Select the matching version from versions list, using semverspec as matching scheme"""

    # Handle special dist tags
    if semver_spec == 'latest':
        semver_spec = dist_tags['latest']
    elif semver_spec == 'next':
        semver_spec = dist_tags['next']
    elif semver_spec == 'experimental':
        semver_spec = dist_tags['experimental']
    elif semver_spec == 'beta':
        semver_spec = dist_tags['beta']
    elif semver_spec == 'rc':
        semver_spec = dist_tags['rc']

    # Remove certain whitespace that causes semver library to crash
    semver_spec = semver_spec.replace('>= ', '>=').replace('< ', '<')

    spec = semantic_version.NpmSpec(semver_spec)

    # Find all matching version and select the highest version
    best = None
    semver_objects = map(semantic_version.Version, versions)
    for version in spec.filter(semver_objects):
        if not best or version > best:
            best = version

    if best:
        return str(best)
    else:
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
    version = select_version(parent_semver, list(package['versions'].keys()), package['dist-tags'])
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

def build_multiple_versions(package, versions):
    for version in versions:
        node = build_tree_from_npm_registry(package, version)
        node.print()
        serialize(node)

# Create and save dependency tree for some package
if __name__ == "__main__":
    #tf_versions = ['0.0.1', '0.15.3', '1.7.4', '2.8.5', '3.21.0', '4.2.0']
    #express_versions =["4.18.2", "5.0.0-beta.1", "3.21.2", "4.0.0", "0.14.1", "1.0.0"]
    #react_versions = ["0.0.1", "0.1.2", "0.14.8", "15.0.0", "15.7.0", "16.0.0-alpha", "17.0.2"]
    cloudainary_versions = ["1.33.0", "1.11.0", "1.1.0", "1.0.1", "0.2.7", "0.0.1"]
    build_multiple_versions("cloudinary", cloudainary_versions)





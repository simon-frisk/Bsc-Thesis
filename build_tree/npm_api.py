import requests
import re
import semantic_version
from dependency_tree.dependency_node import DependencyNode
from dependency_tree.serialize import serialize

NPM_REGISTRY_API_URL = 'https://registry.npmjs.org/{}'

package_cache = {}

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
        raise Exception(f'No matching version was found: {semver_spec}')

def fetch_dependency_from_npm_registry(package):
    """Get package data from npm registry for a javascript package"""

    # Try get from cache
    if package in package_cache:
        return package_cache[package]

    # Get data from npm registry
    response = requests.get(NPM_REGISTRY_API_URL.format(package))
    if response.status_code != 200:
        raise Exception("Failed to fetch package")
    package_json = response.json()

    # Save to cache
    package_cache[package] = package_json

    return package_json


def select_dependency_version_data(package, parent_semver):
    '''Create dependency tree node and dependency list for a version of a package'''
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

    # Return a DependencyNode and the dictionary with dependencies
    return node, dependencies


def build_nested_dependencies(parent_node, dependency_dict):
    """Recursive function to fetch and add dependencies to the tree"""
    for dependency in dependency_dict:
        dependency_package = fetch_dependency_from_npm_registry(dependency)
        dependency_node, nest_dependencies = select_dependency_version_data(dependency_package, dependency_dict[dependency])
        parent_node.add_dependency(dependency_node)
        build_nested_dependencies(dependency_node, nest_dependencies)


def select_analyze_versions(package):
    '''Automatically select which versions should be analyzed'''
    versions = package["versions"].keys()
    versions = list(filter(lambda v: re.match("^\d+.\d+.\d+$", v), versions))
    versions.sort()
    return versions

    selected_versions = []
    current_major = -1
    for (i, version) in enumerate(versions):
        if int(version.split(".")[0]) != current_major:
            if current_major != -1:
                selected_versions.append(versions[i-1])
            selected_versions.append(version)
            current_major = int(version.split(".")[0])
    return selected_versions

def build_from_npm_registry(package):
    '''Build trees for a package'''
    root_package = fetch_dependency_from_npm_registry(package)
    versions = select_analyze_versions(root_package)
    print("Selected versions for", package, versions)

    trees = []

    for version in versions:
        try:
            root_node, root_dependencies = select_dependency_version_data(root_package, version)
            build_nested_dependencies(root_node, root_dependencies)
            trees.append(root_node)
            print(f'Loaded {package} version {version}')
        except:
            print(f'Failed to load {package} version {version}')

    return trees


def load_packages():
    '''Load and save all packages in packages.txt'''

    # Todo : Make run concurrently, non blocking requests in versions and packages

    packages_file = open("packages.txt", "r")
    packages = packages_file.read().split("\n")
    package_list = []
    for package_name in packages:
        print(f'Loading {package_name} ---------------------------------')
        tree_list = build_from_npm_registry(package_name)
        package_list.append(tree_list)
    serialize(packages, package_list)


# Create and save dependency trees
if __name__ == "__main__":
    load_packages()





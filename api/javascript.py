import requests

NPM_REGISTRY_API_URL = 'https://registry.npmjs.org/{}'


def fetch_node(package, version):
    '''
    Function for creating a dependency graph node for a javascript package
    Calls npmjs registry api to get package data including dependencies
    '''

    response = requests.get(NPM_REGISTRY_API_URL.format(package))

    if response.status_code != 200:
        raise "Failed to fetch package"
    package = response.json()

    version_data = package['versions'][version]


def build_tree(package):
    '''
    Create dependency tree for a package, and store it to disk. 
    Also returns the tree
    '''
    pass


if __name__ == "__main__":
    fetch_node('aws-dk', '0.9.0-pre.1')

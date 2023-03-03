
def size_list(dataset):
    size_list = []
    for package in dataset.values():
        dep_list = []
        _get_size(package[-1], dep_list)
        size_list.append([len(dep_list), package[-1].name])
        if package[-1].name == 'ember-cli-babel':
            print(dep_list)

    size_list.sort()
    print(size_list)
    return

def _get_size(node, list):
    if node.name not in list:
        list.append(node.name)
    if node.dependencies != []:
        for dependency in node.dependencies:
            _get_size(dependency, list)

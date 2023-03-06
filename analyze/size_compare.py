
def size_list(dataset):
    size_list = []
    for package in dataset.values():
        dep_list = []
        _get_size(package[-1], dep_list)
        num_versions = 0
        for version in package:
            num_versions += 1
        size_list.append( [package[-1].name, package[-1].version, num_versions, len(dep_list)])
        #if package[-1].name == 'ember-cli-babel':
            #print(dep_list)

    #size_list.sort()
    print(size_list)
    return

def _get_size(node, list):
    if node.name not in list:
        list.append(node.name)
    if node.dependencies != []:
        for dependency in node.dependencies:
            _get_size(dependency, list)


def depth_of_tree(node):
    dep_list = []
    depth_dictionary = {}
    _dfs_depth(dep_list, depth_dictionary, node, 0)
    max_depth = 0
    for key in depth_dictionary.keys():
        if depth_dictionary[key] > max_depth:
            max_depth = depth_dictionary[key]

    return max_depth


def _dfs_depth(list, dictionary, node, depth):
    if node.name not in list:
        list.append(node.name)
        dictionary[node.name] = depth
    else:
        if dictionary[node.name] > depth:
            dictionary[node.name] = depth
    if node.dependencies != []:
        for dependency in node.dependencies:
            _dfs_depth(list, dictionary, dependency, depth+1)


def size_compare():
    biggest_packages = ['ember-cli-babel', 'yeoman-generator', 'webpack', 'mocha', 'yargs', 'gulp-util', 'inquirer', 'express', 'superagent', 'winston', 'shelljs', 'yosay','mongodb', 'vue','aws-sdk','cheerio','body-parser','redis']

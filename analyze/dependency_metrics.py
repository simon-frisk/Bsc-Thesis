def tree_depth_and_edges(node):
    '''Takes a root node and returns a list [tree_depth, tree_edges]'''
    depth_list = []
    _dfs_depth(node, depth_list, 0)
    return [max(depth_list), len(depth_list)-1]


def _dfs_depth(node, list, depth):
    '''Help function for finding tree depth and edges'''
    if node.dependencies == []:
        list.append(depth)
    else:
        for dependency in node.dependencies:
            _dfs_depth(dependency, list, depth+1)
        list.append(depth)


def find_new_dependencies(previous_root, new_root):
    '''Given two trees, function returns a list of lists consisting of new dependencies in the tree,
    in the form of [dependency name, depth level in tree, [depth,edges]of branch below new dependency, parent dependency name'''
    #Should it just return the branch instead?
    old_tree_dependencies = []
    _dependency_name_list(previous_root, old_tree_dependencies)
    new_dependencies = []
    _dependency_compare(new_root, new_dependencies, old_tree_dependencies, new_root.name)
    return new_dependencies

def _dependency_name_list(node, list):
    '''Help function that transforms dependency tree into a list of all dependency names'''
    list.append(node.name)
    if node.dependencies != []:
        for dependency in node.dependencies:
            _dependency_name_list(dependency, list)

def _dependency_compare(node, list, previous_tree_list, parent_name, depth=0):
    '''Iterative help function that finds new dependencies in a tree'''
    if node.dependencies != []:
        for dependency in node.dependencies:
            if dependency.name not in previous_tree_list:
                list.append([dependency.name,depth+1,tree_depth_and_edges(dependency),parent_name])
            else:
                _dependency_compare(dependency, list, previous_tree_list,dependency.name, depth+1)







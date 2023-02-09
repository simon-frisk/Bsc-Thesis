def tree_depth_and_edges(node):
    '''Takes a root node and returns tree depth & size (number of edges)'''
    depth_list = []
    _dfs_depth(node, depth_list, 0)
    return max(depth_list), len(depth_list)-1


def _dfs_depth(node, list, depth):
    if node.dependencies == []:
        list.append(depth)
    else:
        for dependency in node.dependencies:
            _dfs_depth(dependency, list, depth+1)
        list.append(depth)








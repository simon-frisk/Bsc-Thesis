import dependency_tree.serialize as serialize
import os
import dependency_tree.dependency_metrics as dependency_metrics


def print_all_versions(package):
    directory_path = os.path.join('../serialized', package)
    files = os.listdir(directory_path)
    files.sort()
    tree_list = []
    for file_name in files:
        dep_tree = serialize.load(os.path.join(directory_path, file_name))
        print(f"\nDependency tree for {package}: {file_name}")
        dep_tree.print()
        tree_list.append(dep_tree)




if __name__ == '__main__':
    print_all_versions('tfjs')
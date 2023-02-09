import dependency_tree.serialize as serialize
import os


def print_all_versions(package):
    directory_path = os.path.join('../serialized', package)
    files = os.listdir(directory_path)
    files.sort()
    for file_name in files:
        dep_tree = serialize.load(os.path.join(directory_path, file_name))
        print(f"\nDependency tree for {package}: {file_name}")
        dep_tree.print()




if __name__ == '__main__':
    print_all_versions('tfjs')
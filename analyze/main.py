import dependency_tree.serialize as serialize
import os


def print_all_versions():
    directory_path = os.path.join('../serialized/prop-types', '')
    files = os.listdir(directory_path)
    files.sort()
    for file_name in files:
        dep_tree = serialize.load(os.path.join(directory_path, file_name))
        print(f"\nDependency tree for: {file_name}")
        dep_tree.print()

def load_data_set():
    directory_path = '../serialized'
    package_dicts = os.listdir(directory_path)
    for package in package_dicts:
        package_dir = os.path.join(directory_path, package)
        files = os.listdir(package_dir)
        files.sort()
        for file_name in files:
            dep_tree = serialize.load(os.path.join(package_dir, file_name))
            dep_tree.print()

if __name__ == '__main__':
    load_data_set()
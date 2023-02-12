import pickle
from datetime import datetime
import os


def serialize(package_names, package_list):
    root_dir = f'../serialized/{datetime.now()}'
    os.mkdir(root_dir)
    for i in range(len(package_list)):
        package_name = package_names[i]
        package = package_list[i]
        package_dir = f'{root_dir}/{package_name}'
        os.mkdir(package_dir)
        for version in package:
            with open(f'{package_dir}/{version.version}.txt', "wb") as outfile:
                pickle.dump(version, outfile)


def load(location):
    with open(location, "rb") as infile:
        return pickle.load(infile)
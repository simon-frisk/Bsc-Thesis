import pickle


def serialize(dependency_node):
    with open(f'../serialized/{dependency_node.name}/{dependency_node.version}.txt', "wb") as outfile:
        pickle.dump(dependency_node, outfile)


def load(location):
    with open(location, "rb") as infile:
        return pickle.load(infile)
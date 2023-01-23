import pickle


def serialize(dependency_node):
    name = "{}:{}".format(dependency_node.name.replace("/",":"), dependency_node.version)
    with open("../serialized/{}".format(name), "wb") as outfile:
        pickle.dump(dependency_node, outfile)


def load(location):
    with open(location, "rb") as infile:
        return pickle.load(infile)
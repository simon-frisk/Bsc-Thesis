
class DependencyNode:

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.children = []

    def add_child(self, node):
        self.children.append(node)

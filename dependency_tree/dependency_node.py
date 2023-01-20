class DependencyNode:

    def __init__(self, name, version, parent_semver):
        self.name = name
        self.version = version
        self.parent_semver = parent_semver  # The version semver as described by parent
        self.dependencies = []

    def add_dependency(self, node):
        self.dependencies.append(node)

    def print(self, indent=0):
        print(" "*indent, "{}: {}, (parent: {})".format(self.name, self.version, self.parent_semver))
        for dependency in self.dependencies:
            dependency.print(indent + 2)


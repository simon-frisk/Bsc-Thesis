import dependency_tree.serialize as serialize

react_dep_tree = serialize.load("../serialized/react:0.0.0-experimental-ee8509801-20230117.txt")
react_dep_tree.print()
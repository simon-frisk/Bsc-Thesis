import dependency_tree.serialize as serialize

react_dep_tree = serialize.load("../serialized/@tensorflow:tfjs:4.2.0.txt")
react_dep_tree.print()
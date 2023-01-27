import dependency_tree.serialize as serialize

react_dep_tree = serialize.load("../serialized/cloudinary.0.0.1.txt")
react_dep_tree.print()
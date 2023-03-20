
def dependency_exists(package, dependency="inherits"):
    num_versions = len(package)
    step_length = 1 / (num_versions - 1)
    X = [i * step_length for i in range(num_versions)]
    bar_segments = []
    current_included = False
    current_segment_start = 0
    for index, version in enumerate(package):
        is_included = _dep_exists(dependency)
        is_switch = current_included == is_included
        if is_switch and index != 0:
            bar_segments.append((current_segment_start * step_length, (index - current_segment_start) * step_length))



def _dep_exists(node, dep_name):
    if node.name == dep_name:
        return True
    elif node.dependencies:
        for dependency in node.dependencies:
            result = _dep_exists(dependency, dep_name)
            if result: return True
    return False
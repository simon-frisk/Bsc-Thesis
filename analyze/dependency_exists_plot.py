import matplotlib.pyplot as plt

def dependency_exists(package, dependency="inherits"):
    num_versions = len(package)
    step_length = 1 / (num_versions - 1)
    X = [i * step_length for i in range(num_versions)]
    bar_segments = []
    previous_included = False
    current_segment_start = 0
    for index, version in enumerate(package):
        is_included = _dep_exists(version, dependency)
        is_switch = previous_included != is_included
        if is_switch and index != 0 and previous_included == True:
            bar_segments.append((current_segment_start * step_length, (index - current_segment_start) * step_length))
        if is_switch:
            current_segment_start = index
        previous_included = is_included
    if previous_included == True:
        bar_segments.append((current_segment_start * step_length, (len(package) - current_segment_start - 1) * step_length))


    return bar_segments, X


def _dep_exists(node, dep_name):
    if node.name == dep_name:
        return True
    elif node.dependencies:
        for dependency in node.dependencies:
            result = _dep_exists(dependency, dep_name)
            if result: return True
    return False


def existence_timeline_plot(dataset):
    fig, ax = plt.subplots()
    y_tick_placements = []
    y_tick_names = []
    skips = 0
    for index, package in enumerate(dataset.values()):
        segments, x = dependency_exists(package)
        if segments == []:
            skips += 1
            continue
        ax.broken_barh(segments, ((index-skips)*5 + 5,3))
        y_tick_placements.append((index-skips)*5 + 6.5)
        y_tick_names.append(package[0].name)

        print(segments)

    ax.set_yticks(y_tick_placements, labels=y_tick_names)
    ax.set_xlabel("Lifetime of package (% of versions)")
    plt.show()

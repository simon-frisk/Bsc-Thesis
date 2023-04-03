import matplotlib.pyplot as plt
import find_common_deps

def dependency_exists(package, dict, dependency="inherits"):
    num_versions = len(package)
    step_length = 1 / (num_versions - 1)
    X = [i * step_length for i in range(num_versions)]
    bar_segments_first = []
    bar_segments_second = []
    bar_segments_third_plus = []
    strokes = []
    previous_included = False
    current_segment_start = 0
    for index, version in enumerate(package):
        is_included = _dep_exists(version, dependency)
        #is_switch = previous_included != is_included
        #if is_included == True:
            #strokes.append((index*step_length,.001))
        #print(package[0].name)
        #print(version.version)
        if is_included:
            depth = dict[dependency][package[0].name][version.version]
            print(depth)
            if depth == 1:
                bar_segments_first.append((index*step_length, step_length))
            elif depth == 2:
                bar_segments_second.append((index*step_length, step_length))
            else:
                bar_segments_third_plus.append((index*step_length, step_length))

        '''if is_switch and index != 0 and previous_included == True:
            depth = dict[dependency][package][version]
            if depth == 1:g
                bar_segments_first.append((current_segment_start * step_length, (index - current_segment_start) * step_length))
            if depth == 2:
                bar_segments_second.append((current_segment_start * step_length, (index - current_segment_start) * step_length))
        if is_switch:
            current_segment_start = index
        previous_included = is_included
    if previous_included == True:
        bar_segments.append((current_segment_start * step_length, (len(package) - current_segment_start - 1) * step_length))'''

    #print(bar_segments_first)
    #print(bar_segments_second)
    #print(bar_segments_third_plus)
    return bar_segments_first, bar_segments_second, bar_segments_third_plus


def _dep_exists(node, dep_name):
    if node.name == dep_name:
        return True
    elif node.dependencies:
        for dependency in node.dependencies:
            result = _dep_exists(dependency, dep_name)
            if result: return True
    return False


def existence_timeline_plot(dataset):
    dependency_dict = find_common_deps.dependency_dictionary_with_versions(dataset)
    fig, ax = plt.subplots()
    y_tick_placements = []
    y_tick_names = []
    skips = 0
    for index, package in enumerate(dataset.values()):
        first_layer, second_layer, third_layer = dependency_exists(package, dependency_dict)
        print(first_layer)
        print(second_layer)
        print(third_layer)
        if first_layer == [] and second_layer == [] and third_layer ==[]:
            skips += 1
            continue
        ax.broken_barh(first_layer, ((index-skips)*5 + 5,3), facecolors ='tab:blue')
        ax.broken_barh(second_layer, ((index - skips) * 5 + 5, 3), facecolors='tab:red')
        ax.broken_barh(third_layer, ((index-skips)*5 + 5,3), facecolors='tab:green')
        y_tick_placements.append((index-skips)*5 + 6.5)
        y_tick_names.append(package[0].name)

    ax.set_yticks(y_tick_placements, labels=y_tick_names)
    ax.set_xlabel("Lifetime of package (% of versions)")
    plt.show()


    #stroke parameter
    # add color based on depth level


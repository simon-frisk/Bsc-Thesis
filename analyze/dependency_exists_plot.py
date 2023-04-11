import matplotlib.pyplot as plt
import find_common_deps
import matplotlib.patches as mpatches

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
    return bar_segments_first[:-1], bar_segments_second[:-1], bar_segments_third_plus[:-1], num_versions


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
    y_tick_sizes = []
    y_tick_place_sizes = []
    skips = 0
    for index, package in enumerate(dataset.values()):
        first_layer, second_layer, third_layer, num_versions = dependency_exists(package, dependency_dict)
        if first_layer == [] and second_layer == [] and third_layer ==[]:
            skips += 1
            continue
        ax.broken_barh(first_layer, ((index-skips)*5 + 5,3), facecolors ='tab:blue')
        ax.broken_barh(second_layer, ((index - skips) * 5 + 5, 3), facecolors='tab:red')
        ax.broken_barh(third_layer, ((index-skips)*5 + 5,3), facecolors='tab:green')
        y_tick_placements.append((index-skips)*5 + 6.5)
        y_tick_names.append(package[0].name)
        y_tick_place_sizes.append((index-skips)*5 + 6.5)
        y_tick_sizes.append(num_versions)
    y_tick_place_sizes.append(123)
    y_tick_sizes.append("")

    ax.set_yticks(y_tick_placements, labels=y_tick_names)
    ax.set_xlabel("Lifetime of package (% of versions)")
    ax.set_ylabel("Name of package")
    ax2 = ax.twinx()
    ax2.set_yticks(y_tick_place_sizes, labels=y_tick_sizes)
    ax2.set_ylabel("Number of Versions")
    blue_patch = mpatches.Patch(color='tab:blue', label='First layer dep')
    red_patch = mpatches.Patch(color='tab:red', label='Second layer dep')
    green_patch = mpatches.Patch(color='tab:green', label='Third+ layer dep')
    ax.legend(handles=[blue_patch,red_patch,green_patch], loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3)

    plt.show()


    #stroke parameter
    # add color based on depth level


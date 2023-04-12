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
    first =0
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
                bar_segments_first.append(((index-1)*step_length, step_length))
                if index ==0:
                    first=1
            elif depth == 2:
                bar_segments_second.append(((index-1)*step_length, step_length))
                if index ==0:
                    first =2
            else:
                bar_segments_third_plus.append(((index-1)*step_length, step_length))
                if index == 0:
                    first =3



    if len(bar_segments_first)>1 or len(bar_segments_second)>1 or len(bar_segments_third_plus)>1:
        if first == 1:
            return bar_segments_first[1:], bar_segments_second, bar_segments_third_plus, num_versions
        elif first ==2:
            return bar_segments_first, bar_segments_second[1:], bar_segments_third_plus, num_versions
        else:
            return bar_segments_first, bar_segments_second, bar_segments_third_plus[1:], num_versions
    else:
        return bar_segments_first, bar_segments_second, bar_segments_third_plus, num_versions

def _dep_exists(node, dep_name):
    if node.name == dep_name:
        return True
    elif node.dependencies:
        for dependency in node.dependencies:
            result = _dep_exists(dependency, dep_name)
            if result: return True
    return False


def existence_timeline_plot(dataset, dependency="inherits"):
    dependency_dict = find_common_deps.dependency_dictionary_with_versions(dataset)
    fig, ax = plt.subplots()
    y_tick_placements = []
    y_tick_names = []
    y_tick_sizes = []
    y_tick_place_sizes = []
    skips = 0
    for index, package in enumerate(dataset.values()):
        first_layer, second_layer, third_layer, num_versions = dependency_exists(package, dependency_dict, dependency)
        if first_layer == [] and second_layer == [] and third_layer ==[]:
            skips += 1
            continue
        ax.broken_barh(first_layer, ((index-skips)*5 + 5,3), facecolors ='tab:blue')
        ax.broken_barh(second_layer, ((index - skips) * 5 + 5, 3), facecolors='tab:red')
        ax.broken_barh(third_layer, ((index-skips)*5 + 5,3), facecolors='tab:green')
        y_tick_placements.append((index-skips)*5 + 6.5)
        y_tick_names.append(package[0].name)
        y_tick_place_sizes.append((index-skips)*5 + 6.5)
        percent_included = round((len(dependency_dict[dependency][package[0].name].keys())/(num_versions))*100, 2)
        '''if package[0].name == 'ember-cli-babel' or :
            percent_included = 100'''
        y_tick_sizes.append(str(num_versions) + " (" + str(percent_included) + ")")

    y_tick_place_sizes.append(5*(len(y_tick_names)+1.63))
    y_tick_sizes.append("")

    ax.set_yticks(y_tick_placements, labels=y_tick_names)
    ax.set_xlabel("Lifetime of package (% of versions)")
    ax.set_ylabel("Name of package")
    ax2 = ax.twinx()
    ax2.set_yticks(y_tick_place_sizes, labels=y_tick_sizes)
    ax2.set_ylabel("Total Number of Versions of Package (% including dep)")
    blue_patch = mpatches.Patch(color='tab:blue', label='First layer dep')
    red_patch = mpatches.Patch(color='tab:red', label='Second layer dep')
    green_patch = mpatches.Patch(color='tab:green', label='Third+ layer dep')
    ax.legend(handles=[blue_patch,red_patch,green_patch], loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3)

    plt.show()


    #stroke parameter
    # add color based on depth level


import matplotlib.pyplot as plt
import violin_plots
import numpy as np





def existence_timeline_scatter(package):
    num_versions = len(package)
    X = [i / (num_versions - 1) for i in range(num_versions)]
    number_of_dependencies = []
    for version in package:
        unique_deps = []
        violin_plots._number_of_deps(version, unique_deps)
        size = len(unique_deps) - 1
        number_of_dependencies.append(size)

    return X, number_of_dependencies

def timeline_scatter_plot(dataset):
    all_x = []
    all_y = []
    fig, ax = plt.subplots()
    for package in dataset.values():
        x,y = existence_timeline_scatter(package)
        #ax.scatter(x,y, s=4)
        ax.plot(x,y)
        all_x += x
        all_y += y
    b, a = np.polyfit(np.array(all_x), np.array(all_y), deg=1)
    xseq = np.linspace(0, 1, num=50)
    ax.plot(xseq, a+b*xseq, color = "black")
    plt.ylabel("Number of dependencies")
    plt.yscale("log")
    plt.xlabel("Lifetime of package")
    plt.show()

def timeline_scatter_plot_size_split(dataset):
    all_big_x = []
    all_big_y = []
    all_small_x = []
    all_small_y = []

    for package in dataset.values():
        x,y = existence_timeline_scatter(package)
        if max(y) > 10:
            all_big_x.append(x)
            all_big_y.append(y)
        else:
            all_small_x.append(x)
            all_small_y.append(y)

    fig, ax = plt.subplots()
    big_x = []
    big_y = []
    for i in range(len(all_big_x)):
        ax.scatter(all_big_x[i],all_big_y[i], s=4)
        #ax.plot(all_big_x[i],all_big_y[i])
        big_x += all_big_x[i]
        big_y += all_big_y[i]
    b, a = np.polyfit(np.array(big_x), np.array(big_y), deg=1)
    xseq = np.linspace(0, 1, num=50)
    ax.plot(xseq, a+b*xseq, color = "black")
    plt.ylabel("Number of dependencies")
    plt.yscale("log")
    plt.xlabel("Lifetime of package")
    plt.title("Packages w/ more than 10 deps at any point")
    plt.show()

    fig, ax = plt.subplots()
    small_x = []
    small_y = []
    for i in range(len(all_small_x)):
        #ax.scatter(all_small_x[i], all_small_y[i], s=4)
        ax.plot(all_small_x[i],all_small_y[i])
        small_x += all_small_x[i]
        small_y += all_small_y[i]
    b, a = np.polyfit(np.array(small_x), np.array(small_y), deg=1)
    xseq = np.linspace(0, 1, num=50)
    ax.plot(xseq, a + b * xseq, color="black")
    plt.ylabel("Number of dependencies")
    # plt.yscale("log")
    plt.xlabel("Lifetime of package")
    plt.title("Packages w/ less than 10 deps at all points")
    plt.show()
    return


def existence_timeline(package):
    num_versions = len(package)
    X = [i / (num_versions - 1) for i in range(num_versions)]
    number_of_dependencies = []
    max = 0
    min = 10000000
    previous_size = -1
    jumps = 0
    for version in package:
        unique_deps = []
        violin_plots._number_of_deps(version, unique_deps)
        size = len(unique_deps) - 1
        number_of_dependencies.append(size)
        if size > max: max = size
        if size < min: min = size
        if version.name == 'yosay':
            print(previous_size)
            print(size)
            print('-------')
        if previous_size == -1:
            previous_size = size
        if size != previous_size:
            jumps+=1
            previous_size=size

    num_deps_copy = number_of_dependencies.copy()
    for i in range(len(number_of_dependencies)):
        number_of_dependencies[i] = (number_of_dependencies[i] - min) / max
        num_deps_copy[i] = (number_of_dependencies[i] - min)
    return X, number_of_dependencies, max, min, jumps


def timeline_plot(dataset):
    name_ticks = []
    min_max_ticks = []
    y_tick_placements =[]
    fig, ax = plt.subplots()
    info_list = []
    for i, package in enumerate(dataset.values()):
        x, y, max, min, jumps = existence_timeline(package)
        name_tick = package[0].name + " (" + str(len(package)) + ")"
        #name_ticks.append(package[0].name + " (" + str(len(package)) + ")")
        #min_max_ticks.append("("+str(min) + ", " +str(max) +")")
        #ax.axhline((2 * i), 0, 1, linestyle="--", color='lightgray', linewidth=1)
        #ax.axhline((2 * i + 1), 0, 1, linestyle="--", color='lightgray', linewidth=1)
        #ax.plot(x, y)
        info_list.append([jumps, x, y, max, min, name_tick])
        y_tick_placements.append((2*i+.5))

    info_list.sort()
    count =0
    for package_info in info_list:
        x = package_info[1]
        number_of_deps = package_info[2]
        for ii in range(len(number_of_deps)):
            number_of_deps[ii] += 2*count
        ax.plot(x, number_of_deps, color="gray")
        ax.axhline((2 * count), 0, 1, linestyle="--", color='lightgray', linewidth=1)
        ax.axhline((2 * count + 1), 0, 1, linestyle="--", color='lightgray', linewidth=1)
        name_ticks.append(package_info[5])
        min_max_ticks.append(str(package_info[0]) + ", (" + str(package_info[4]) + ", " + str(package_info[3]) + ")")
        count +=1



    ax.set_yticks(y_tick_placements, labels=name_ticks)
    ax.set_ylabel("Name of Package (# Versions)")
    ax.set_xlabel("Lifetime of Package")
    ax.set_xlim([0,1])
    y_tick_placements.append(133.3)
    min_max_ticks.append("")
    y_tick_placements.append(-6.5)
    min_max_ticks.append("")
    ax2 = ax.twinx()
    ax2.set_yticks(y_tick_placements, labels=min_max_ticks)
    ax2.set_ylabel("# of Jumps, (Min, Max #Dependencies)")
    plt.show()




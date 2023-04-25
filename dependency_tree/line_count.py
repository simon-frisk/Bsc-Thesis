import matplotlib.pyplot as plt
import csv
import os
import subprocess
import io


def package_line_counts():
    packages_file = open("../build_tree/packages.txt", "r")
    packages = packages_file.read().split("\n")
    git_folders = os.listdir('../repos')
    code_lines = {}
    for package_name in packages:
        if package_name not in git_folders:
            continue
        results = subprocess.run(["cloc", f"../repos/{package_name}", '--csv'], capture_output=True, text=True)
        out_idx = results.stdout.find("files,language")
        out = io.StringIO(results.stdout[out_idx:])
        csv_reader = csv.reader(out, delimiter=',')
        for row in csv_reader:
            if row is [] or len(row) < 2:
                continue
            elif row[1] == "JavaScript" or row[1] == "TypeScript":
                if package_name not in code_lines:
                    code_lines[package_name] = 0
                code_lines[package_name] += int(row[4])

    return code_lines


def print_package_code_lines(code_lines_dict):
    for package in code_lines_dict:
        print(f"{package:{30}}{code_lines_dict[package]} lines")


def line_count_violin_plot(code_lines_dict):
    plt.violinplot(code_lines_dict.values(), showmedians=True, quantiles=[0.25, 0.5, 0.75])
    plt.ylabel("No. Lines of Code")
    plt.title("Distribution of No. Lines of Code")
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":
    line_counts = package_line_counts()
    print(len(line_counts))
    print_package_code_lines(line_counts)
    #line_count_violin_plot(line_counts)

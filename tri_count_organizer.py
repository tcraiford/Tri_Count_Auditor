import os
import subprocess
import sys

required = ["trimesh", "fbxloader", "PySide6"]
missing = []
for i in required:
    try:
        globals()[i] = __import__(i)
    except:
        missing.append(i)
if missing:
    print(f"Missing libraries: {', '.join(missing)}")
    answer = input("Do you wish to install them now? [y/n] ")
    if answer.lower() == "y":
        for i in missing:
            subprocess.run(["pip", "install", i])
        print("Installation complete. Relaunching now...")
        subprocess.run([sys.executable, __file__])
        sys.exit()
    else:
        sys.exit()

from fbxloader import FBXLoader

def get_directory():
    directory = input("Enter directory to scan: ")
    while not os.path.exists(directory):
        print("Directory does not exist or is unreachable.")
        directory = input("Enter a directory path:")
    return directory

def scan_files(directory, supported_formats):
    my_list = []
    for root, dirs, files in os.walk(directory):
        for item in files:
            if item.endswith(supported_formats):
                my_list.append(os.path.join(root, item))
    if not my_list:
        print("No supported geometry files in this directory.")
    return my_list

def get_tri_counts(my_list, directory):
    file_count = {}
    failed_load = []
    for item in my_list:
        base_name = os.path.relpath(item, directory)
        print(f"Scanning {base_name}")
        #if file's a fbx, load into variable fbx by FBXLoader and put into variable model otherwise assume as obj
        try:
            if item.endswith(".fbx"):
                fbx = FBXLoader(item)
                model = fbx.export_trimesh()
            else:
                model = trimesh.load(item)
            tri_count = len(model.triangles)
            #takes the dict, file_count, and makes base_name the key and tri_count the value for that key
            file_count[base_name] = tri_count
        except:
            print("\033[35m" + f"Failed to load {base_name}. Moving to next item." + "\033[0m")
            failed_load.append(base_name)
    return file_count, failed_load

def display_results(file_count, sort_type, green, threshold, failed_load):
    green_count = 0
    yellow_count = 0
    red_count = 0
    if sort_type == "a":
        sorted_files = sorted(file_count.items(), key = lambda x: x[0])
    else:
        sorted_files = sorted(file_count.items(), key = lambda x: x[1])

    for key, value in sorted_files:
        name_length = 60 - len(key)
        if name_length > 0:
            dots = "." * name_length
        else:
            dots = ""
            key = (f"{key[:33]}...{key[-4:]}")
        if value < green:
            print("\033[32m" + f"{key}{dots} |{value}" + "\033[0m")
            green_count += 1
        elif value < threshold:
            print("\033[33m" + f"{key}{dots} |{value}" + "\033[0m")
            yellow_count += 1
        else:
            print("\033[31m" + f"{key}{dots} |{value}" + "\033[0m")
            red_count += 1
    print(f"{green_count} bellow 50% threshold / {yellow_count} 50%-99% threshold / {red_count} above threshold")
    print(f"{len(failed_load)} failed to load")

def sort_choice():
    while True:
        sort_type = input("Enter [a] to sort alphabetically or [n] to sort numerically: ").strip().lower()
        if sort_type in ["a", "n", ""]:
            return sort_type

def set_threshold():
    threshold = input("Enter triangle count threshold: [default 100000] ")
    #assigns the thresholds for each color based on user input threshold
    if not threshold:
        green = 50000
        threshold = 100000
    else:
        threshold = int(threshold)
        green = threshold // 2
    return (threshold, green)

def new_sort_threshold(threshold, green, sort_type, failed_load):
    new_directory = False
    answer = input(f"[l] to list failed\n"
                f"[nd] to change directory\n"
                f"[t] to change threshold\n"
                f"[a] to sort alphabetically\n"
                f"[n] to sort numerically\n"
                f"{'_' * 60}\n").strip().lower()
    while answer not in ["nd", "t", "a", "n", "l"]:
        answer = input().strip().lower()
    if answer == "a":
        sort_type = "a"
    elif answer in ["n", ""]:
        sort_type = "n"
    elif answer == "t":
        threshold, green = set_threshold()
    elif answer == "nd":
        new_directory = True
    elif answer == "l":
        print("\033[35m" + f"Failed to load:\n"
              f"{failed_load}" + "\033[0m")
        input("Press Enter to continue...")
    return (threshold, green, sort_type, new_directory)

def main():
    while True:
        directory = get_directory()
        threshold, green = set_threshold()
        my_list = scan_files(directory, supported_formats)
        sort_type = sort_choice()
        file_count, failed_load = get_tri_counts(my_list, directory)
        while True:
            display_results(file_count, sort_type, green, threshold, failed_load)
            print("_" * 40)
            threshold, green, sort_type, new_directory = new_sort_threshold(threshold, green, sort_type, failed_load)
            if new_directory == True:
                break

supported_formats = (".obj", ".fbx", ".glb", ".gltf", ".stl")

if __name__ == "__main__":
    main()

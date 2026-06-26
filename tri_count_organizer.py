import os
import subprocess
import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QFileDialog)
from PySide6.QtGui import(QColor)

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


def scan_files(directory, supported_formats):
    my_list = []
    for root, dirs, files in os.walk(directory):
        for item in files:
            if item.endswith(supported_formats):
                my_list.append(os.path.join(root, item))

    return my_list

def get_tri_counts(my_list, directory):
    file_count = {}
    failed_load = []
    for item in my_list:
        base_name = os.path.relpath(item, directory)


        #if file is a fbx, load into variable fbx by FBXLoader and put into variable model otherwise assume as obj
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
            failed_load.append(base_name)
    return file_count, failed_load


#defines the class MainWindow which is called by the if main bellow
#creates the default values for each of the new variables we're creating inside self
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triangle Count Organizer")
        self.directory = ""
        self.sort_type = "n"
        self.file_count = {}
        self.failed_load = []
        self.user_threshold = QLineEdit("Threshold (100000)")
        self.user_threshold.returnPressed.connect(self.populate_table)
        self.directory_line = QLineEdit()
        self.directory_line.returnPressed.connect(self.scan_and_populate_table)
        self.results_table = QTableWidget(1, 2)
        self.results_table.setHorizontalHeaderLabels(["File Name", "Triangle Count"])
        self.failure_label = QLabel("")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout main_layout is where all the individual widgets and row/collum layouts get added to
        main_layout = QVBoxLayout(central_widget)

        # Create a label widget and add it to main_layout
        description = QLabel("Scan a directory for 3D geo files and display triangle counts")

        # Create buttons that don't need self. Then tell them what they do by connecting them to their method
        open_dir_button = QPushButton("Open Directory")
        open_dir_button.clicked.connect(self.open_directory)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_window)
        threshold_button = QPushButton("Set Threshold")
        threshold_button.clicked.connect(self.populate_table)
        scan_button = QPushButton("Scan")
        scan_button.clicked.connect(self.scan_and_populate_table)

        # Create the layout dir_layout and then add each widget to it individually
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.directory_line)
        dir_layout.addWidget(browse_button)
        dir_layout.addWidget(open_dir_button)



        # Create the layout scan_layout and then add the scan widget to it
        scan_layout = QHBoxLayout()
        scan_layout.addWidget(self.user_threshold)
        scan_layout.addWidget(threshold_button)
        scan_layout.addWidget(scan_button)


        # Define the order of the items added to the main window
        main_layout.addWidget(description)
        main_layout.addLayout(dir_layout)
        main_layout.addLayout(scan_layout)
        main_layout.addWidget(self.results_table)
        main_layout.addWidget(self.failure_label)
        self.failure_label.hide()
        # Enables sorting by clicking the header of the table
        self.results_table.setSortingEnabled(True)

    def browse_window(self):
        user_directory = QFileDialog.getExistingDirectory()
        self.directory_line.setText(user_directory)
        self.scan_and_populate_table()

    def open_directory(self):
        directory = self.directory_line.text()
        os.startfile(directory)

    def scan_user_directory(self):
        # Once scan button pressed, this takes whatever is in self.directory_line input and defines directory with it
        directory = self.directory_line.text()
        # Call the functions from the cli using the new inputted directory from the gui
        my_list = scan_files(directory, supported_formats)
        self.file_count, self.failed_load = get_tri_counts(my_list, directory)

    def populate_table(self):
        # Establish Hex codes as easy variables
        red = "#ff0800"
        green = "#4cbb17"
        yellow = "#fce205"

        # If user doesn't put in valid threshold, it will default to 100000
        try:
            threshold = int(self.user_threshold.text())
        except:
            threshold = 100000

        # Disables sorting while table is being populated. Need to re-enable after
        self.results_table.setSortingEnabled(False)

        if self.failed_load:
            self.failure_label.show()
            self.failure_label.setText(f"{len(self.failed_load)} failed to load.")
        else:
            self.failure_label.hide()

        row_val = 0
        self.results_table.setRowCount(len(self.file_count))
        for key, val in self.file_count.items():
            # Convert key and val to QTable items that we can apply a QColor to
            line_key = QTableWidgetItem(key)
            line_val = QTableWidgetItem(str(val))
            # Determine what Color the text should be
            if int(val) > threshold:
                color = red
            elif int(val) < (threshold // 2):
                color = green
            else:
                color = yellow

            line_key.setForeground(QColor(color))
            line_val.setForeground(QColor(color))

            self.results_table.setItem(row_val, 0, line_key)
            self.results_table.setItem(row_val, 1, line_val)
            row_val += 1

        # Re-enable sorting by clicking on header after table is filled
        self.results_table.setSortingEnabled(True)

    def scan_and_populate_table(self):
        self.scan_user_directory()
        self.populate_table()



supported_formats = (".obj", ".fbx", ".glb", ".gltf", ".stl")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
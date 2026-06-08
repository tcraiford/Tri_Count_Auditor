tri_count_organizer
A standalone Python CLI tool for scanning directories of 3D asset files and reporting triangle counts per file. Designed for game development and archviz pipelines to quickly identify heavy or unoptimized geometry before importing assets into Unreal Engine or other real-time applications.
---
What It Does
Point it at a directory, and it will:
Recursively scan for supported 3D file formats
Extract the triangle count from each file
Color-code results against a user-defined threshold (green / yellow / red)
Sort results alphabetically or by triangle count
Display results with aligned dot-leader columns and relative file paths
Report a summary of scanned files by color category
Handle corrupt or unreadable files without crashing
---
Motivation
In production pipelines, heavy geometry is one of the most common causes of performance issues in real-time engines. Identifying problematic assets before they enter the engine — rather than after — saves significant iteration time. This tool was built to fill that gap: a lightweight, standalone scanner that requires no DCC software to run.
---
Supported Formats
Format	Notes
`.obj`	Fully supported via trimesh
`.fbx`	Binary FBX supported via fbxloader. ASCII FBX not currently supported — planned for a future update
`.glb`	Fully supported via trimesh
`.gltf`	Supported via trimesh. Requires companion `.bin` file to be present in the same directory
`.stl`	Fully supported via trimesh
---
Requirements
Python 3.10+
trimesh
fbxloader
numpy (installed automatically as a trimesh dependency)
Dependencies are checked at launch. If any are missing, the tool will offer to install them automatically before relaunching.
---
Installation

No manual pip installs required — the tool handles missing dependencies on first run.
---
Usage
Run the script directly in Windows or from the command line:

python tri_count_organizer.py


You will be prompted to:
Enter a directory path to scan
Set a triangle count threshold (default: 100,000)
Choose a sort order — alphabetical or numerical (default: numerical)
Results are displayed with color coding:
🟢 Green — below 50% of threshold (optimized)
🟡 Yellow — between 50% and 100% of threshold (moderate)
🔴 Red — at or above threshold (heavy, review recommended)
After results are displayed, you can interactively:
Change sort order without rescanning
Adjust the threshold and re-display results
Switch to a different directory
List any files that failed to load
---
Threshold Logic
The default threshold of 100,000 triangles is grounded in real decimation workflow reasoning. In archviz and game asset production, dense geometry such as rockwork is typically decimated to approximately 50,000 vertices — which corresponds to roughly 100,000 triangles on the low end. Files below half the threshold are considered well-optimized; files at or above the threshold warrant review before engine import.
---
Known Limitations
ASCII FBX files are not currently supported. fbxloader 0.0.2 handles binary FBX only. ASCII FBX support is planned for a future update.
GLTF files require their companion `.bin` file to be present in the same directory as the `.gltf` file.
Filenames exceeding approximately 55 characters will be truncated in the display output. This is a CLI display limitation and will be resolved in the planned GUI version.
Triangle counts may differ slightly from DCC software counts for skinned meshes loaded via fbxloader.
---
Roadmap
[ ] PySide6 GUI wrapper with directory browser and interactive results panel
[ ] ASCII FBX support
[ ] Per-file relative path display in GUI with directory navigation
[ ] HTML/CSV export of scan results
---
About
Built as a portfolio piece targeting technical artist and pipeline TD roles in game development. Developed in Python as a standalone tool requiring no DCC software, designed to fit into automated pre-import validation pipelines.
Author: Taylor Raiford
Portfolio: taylorraiford.com

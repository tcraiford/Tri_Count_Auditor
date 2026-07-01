# Triangle Count Auditor

A standalone Python tool for scanning directories of 3D asset files and reporting triangle counts per file. Built for game development and archviz pipelines to quickly identify heavy or unoptimized geometry before importing assets into a real-time engine.

## What It Does

Point it at a directory and it will:

- Recursively scan for supported 3D file formats up to a configurable folder depth
- Extract the triangle count and file size from each file
- Color-code results against a user-defined threshold (green / yellow / red)
- Display results in a sortable table by file name, triangle count, or file size
- Report any files that failed to load without crashing
- Run without any DCC software installed

## Why It Exists

In production pipelines, heavy geometry is one of the most common causes of performance issues in real-time engines. Identifying problematic assets before they enter the engine — rather than after — saves significant iteration time. This tool is a lightweight, standalone auditor that any team member can run regardless of whether they have Maya, 3ds Max, or any other DCC license.

## Supported Formats

| Format | Notes |
|--------|-------|
| `.obj` | Fully supported via trimesh |
| `.fbx` | Binary FBX supported via fbxloader. ASCII FBX not currently supported |
| `.glb` | Fully supported via trimesh |
| `.gltf` | Supported via trimesh. Requires companion `.bin` file in the same directory |
| `.stl` | Fully supported via trimesh |

## Requirements

- Python 3.10+
- PySide6
- trimesh
- fbxloader
- numpy (installed automatically as a trimesh dependency)

Dependencies are checked at launch. If any are missing, the tool will offer to install them automatically before relaunching.

## Installation

No manual pip installs required — the tool handles missing dependencies on first run.

## Usage

Run the script directly:

```
python tri_count_organizer.py
```

1. Enter or browse to a directory
2. Optionally set a scan depth limit (default: 4)
3. Optionally set a triangle count threshold (default: 100,000)
4. Click Scan

Results are color-coded:
- 🟢 **Green** — below 50% of threshold (well optimized)
- 🟡 **Yellow** — between 50% and 100% of threshold (moderate)
- 🔴 **Red** — at or above threshold (review recommended)

Click any column header to sort results. Adjust the threshold and click Set Threshold to recolor results without rescanning.

## Threshold Logic

The default threshold of 100,000 triangles is grounded in real decimation workflow reasoning. In archviz and game asset production, dense geometry is typically decimated to approximately 50,000 vertices — roughly 100,000 triangles on the low end. Files below half the threshold are considered well optimized; files at or above warrant review before engine import.

## Known Limitations

- ASCII FBX files are not currently supported. fbxloader handles binary FBX only
- GLTF files require their companion `.bin` file in the same directory
- Triangle counts may differ slightly from DCC software counts for skinned meshes loaded via fbxloader

## Roadmap

- [ ] ASCII FBX support
- [ ] HTML / CSV export of scan results
- [ ] Right-click to copy file path from results table

## About

Built as a portfolio piece targeting technical artist and pipeline TD roles in game development. Developed in Python as a standalone tool requiring no DCC software, designed to fit into pre-import validation workflows.

**Author:** Taylor Raiford
**Portfolio:** taylorraiford.com

# Aviation GIS Tools

Python tools for working with aviation and geospatial data.

**aviation-gis-tools** provides utilities commonly used when processing aeronautical publications and aviation-related geographic data, including:
* Coordinate conversion between different formats, e.g. DMS → DD
* Distance conversion between different units, e.g. km, NM, and feet
* Coordinate extraction from plain text, such as aeronautical publications (NOTAM, eAIP)
* Coordinate calculations based on point locations, bearings, and distances commonly used in aeronautical publications

# Why Aviation GIS Tools?

Aviation data frequently uses coordinate and measurement formats that differ from those commonly used by GIS and general-purpose Python libraries.
This package provides small, focused utilities for bridging the gap between:
* aeronautical publications,
* aviation data,
* GIS applications, and
* standard geographic coordinate representations.

# Development setup

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

## Prerequisites

* Python
* Poetry

## Setup

* Clone the repository and install the project dependencies:
```commandline
git clone <repository-url>
cd aviation-gis-tools
poetry install
```

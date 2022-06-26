# Pylidar

## Introduction

<p>
 Pylidar enables accessing USGS 3DEP LiDAR point clouds data from registry of open data on AWS and allows proccessing of the lidar data.
</p>


**Table of content**

 [Pylidar](#Pylidar)
  - [Overview](#overview)
  - [Data Source](#data-Source)
  - [Requirements](#requirements)
  - [Installation Guide](#installation-guide)
  - [Project Structure](#project-structure)
    - [src](#src)
        - [assets](#assets)
    - [docs](#docs)
    - [tests](#tests)


## Overview

<p>
This project aims to produce an easy to use, reliable and well designed python module that domain experts and data scientists can use to fetch, visualize, and transform publicly available satellite and LIDAR data.
</p>

## Data Source
<p>
Data Source for this project comes from AWS Public Dataset of the USGS 3DEP LiDAR point cloud data.
Link For data set - https://registry.opendata.aws/usgs-lidar/
</p>

## Requirements
<p>
 PDAL
 Geopandas
</p>

## Installation Guide

For the time being cloning is the only option (will be updated once the package is ready) 
        ```bash
            git clone https://github.com/tesfayealex/Pylidar
            cd Pylidar
            pip install -r requirements.txt
        ```
  
## Project Structure
The Project uses a recomended python package project structure which includes

### src 
This folder holds the lidar metadata generator , processor , data transformer modules and assets
- `lidar_data_processor.py`: a python script for processing lidar data
- `lidar_metadata_generator.py`: a python script for generating metadata from the lidar data source
- `transformation_utility.py`: a python script for lidar data transformation
### assets
This folder holds the metadata generated , pipeline template and filenames of data source
- `datasource_filenames.txt`: text file with data source file names
- `metadata.csv`: csv data of the lidar metadata 
- `pipeline_template.json`: pdal pipeline template file
### docs 
This folder holds package documentation
### tests
This folder holds unit test files
- `test_lidar_data_processor.py`: unit test file for lidar data processing python script
- `test_transformation_utility.csv`: unit test file for lidar data transformation python script

## Install from TestPyPi repository
    - `pip install -i https://test.pypi.org/simple/ pylidar`

## Used Reference and Reused Codes From
    - https://towardsdatascience.com/how-to-automate-lidar-point-cloud-processing-with-python-a027454a536c




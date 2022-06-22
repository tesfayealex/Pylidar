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
### assets
    This folder holds the metadata generated , pipeline template and filenames of data source
### docs 
    This folder holds package documentation
### tests
    This folder holds unit test files

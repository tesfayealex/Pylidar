import os
import pandas as pd
import numpy as np
import pdal
import json
from shapely.geometry import Polygon , Point
import geopandas as gpd


class Lidar_Processor():

    def __init__(self , region: str='', polygon_array: list = [], epsg: int = 3857 ,default_epsg: int = 3857):
        """ Initializes the class with region , polygon array and EPSG Amount

        Args:
            region (String): Point cloud data location name on the AWS cloud storage EPT resource. 
            polygon (Polygon): Geometry object describing the boundary of the requested location.
            epsg (Integer): Output EPSG of the Point Cloud data
            default_epsg (Integer): Input EPSG of the Point Cloud data

        Returns:
        None
        """
        polygon = Polygon()
        if polygon_array != []:
            MINX, MINY, MAXX, MAXY = polygon_array
            polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))

        self.polygon = polygon
        self.pipeline={}
        self.epsg = epsg
        self.default_epsg = default_epsg
        self.region = region
        self.pipeline_template_path = '../src/assets/pipeline_template.json'
        self.metadata_path = "../src/assets/metadata.csv"
    
    def pipline_modifier(self):
        """ Modifies the PDAL pipeline template to the required region PDAL template

        Args:
        None    

        Returns:
            list: List of pipeline template with modified parameters
        """
        with open(self.pipeline_template_path, 'r') as json_file:
            pipeline = json.load(json_file)
        bound = ()
        region_data = {}
        if self.region != "":
                bound, region_data = self.get_region_from_name()
                if len(region_data) == 0:
                    bound , region_data
        
        if self.region == '' or len(region_data) == 0:
            bound , region_data = self.get_region_from_boundary()

        if len(region_data) != 0:
                self.pipeline = pipeline
                self.pipeline['pipeline'][0]['filename'] = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"+ region_data['region'] + "/ept.json"
                self.pipeline['pipeline'][0]['bounds'] = "(" + str([bound[0],bound[1]]) + "," + str([bound[2],bound[3]]) + ")"
                self.pipeline['pipeline'][3]['out_srs'] = f'EPSG:{self.epsg}'
                self.pipeline['pipeline'][6]['filename'] = '../src/assets/data/'+ str(region_data['region'] + ".laz")
                self.pipeline['pipeline'][7]['filename'] = '../src/assets/data/'+ str(region_data['region'] + ".tif")
                return self.pipeline['pipeline']
                
        else:
                return []

    def pipline_executer(self):
        """ Executes the PDAL pipeline to fetch lidar point cloud data from the AWS cloud storage. 

        Args:
        None

        Returns:
            list: List of point clouds fetched from AWS
        """
        self.pipline_modifier()
        pipeline = pdal.Pipeline(json.dumps(self.pipeline))
        pipeline.execute()
        self.pipeline_array = pipeline.arrays[0]
        return self.pipeline_array

    def get_geo_df(self, array_data: np.ndarray) -> gpd.GeoDataFrame:
        """ Creates Dataframe from the PDAL pipeline array 

        Args:
            array_data (Numpy Array): Numpy array of point clouds from pdal pipeline
        Returns:
            geopandas dataframe:  geopandas dataframe of the downloaded region
        """
        geometry_points = [Point(x, y) for x, y in zip(array_data["X"], array_data["Y"])]
        elevations = array_data["Z"]

        geo_df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
        geo_df['elevation'] = elevations
        geo_df['geometry'] = geometry_points
        geo_df = geo_df.set_geometry("geometry")
        geo_df.set_crs(epsg=self.epsg, inplace=True)
        return geo_df

    def get_region_from_name(self):
        """ Identifies the required region from the region name 
        Args:
        None

        Returns:
            Tuple: Tuple of bounds of the identified region
            JSON: json of the full region data from the metadata
        """
        metadata = pd.read_csv(self.metadata_path)
        for index in range(len(metadata)):
                row = metadata.iloc[index]  
                if row['fileanme'] == self.region:
                    bound_tuple = (row['xmin'],row['xmax'],row['ymin'],row['ymax'])
                    return bound_tuple , region_data
        return (),{}

    def get_region_from_boundary(self):
        """ Identifies the required region from the polygon boundary 
        Args:
        None

        Returns:
            Tuple: Tuple of bounds of the identified region
            JSON: json of the full region data from the metadata
        """
        polygon_df = gpd.GeoDataFrame([self.polygon], columns=['geometry'])
        polygon_df.set_crs(epsg=self.epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.default_epsg)
        xmin, ymin, xmax, ymax = polygon_df['geometry'][0].bounds
        bound_tuple = (xmin, xmax, ymin, ymax)
        x_cord, y_cord = polygon_df['geometry'][0].exterior.coords.xy
        polygon_str = f"({x_cord},{y_cord})"
        metadata = pd.read_csv(self.metadata_path)
        for index in range(len(metadata)):
                row = metadata.iloc[index]  
                if row['xmin'] <= xmin and row['xmax'] >= xmax and row['ymin'] <= ymin and row['ymax'] >= ymax:
                        region_data = row
                        return bound_tuple , region_data
        return () , {} 

    def fetch_file(self):
        """ Main function that fetches lidar point cloud data from EPT resources from AWS cloud storage. 

        Args:
        None 

        Returns:
            Dataframe: Geopandas data frame for the identified region
            String: Path of the downloaded tiff file
            list: Pipeline array of the found region
        """
        pipeline_array = self.pipline_executer()
        self.geo_df = self.get_geo_df(pipeline_array)
        tiff_path = os.path.abspath(self.pipeline['pipeline'][7]['filename'])
        return self.geo_df , tiff_path , pipeline_array

if __name__ == "__main__":
        polygon_array = [446112.3120340019  , 4652575.060161518 , 447610.6998241764,4654067.900678839]
        processor = Lidar_Processor( polygon_array,'Pylidar/src/assets/pipeline_template.json', 'Pylidar/src/assets/metadata.csv', epsg=26915)
        pipeline_array = processor.pipline_executer()
        geo_df = processor.get_geo_df(pipeline_array)
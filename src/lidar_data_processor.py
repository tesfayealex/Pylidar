import pandas as pd
import numpy as np
import pdal
import json
from shapely.geometry import Polygon , Point
import geopandas as gpd


class Lidar_Processor():

    def __init__(self , pipeline_template_path , metadata_path , polygon , epsg):
        self.pipeline_template_path = pipeline_template_path
        self.metadata_path = metadata_path
        self.polygon = polygon
        self.pipeline={}
        self.epsg = epsg
        self.default_epsg = "3857"
    def pipline_modifier(self):
        pass

    def get_region_from_boundary(self):
        polygon_df = gpd.GeoDataFrame([self.polygon], columns=['geometry'])
        polygon_df.set_crs(epsg=self.epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.default_epsg)
        xmin, ymin, xmax, ymax = polygon_df['geometry'][0].bounds
        # bound = Bounds(xmin, xmax, ymin, ymax)
        bound_tuple = (xmin, xmax, ymin, ymax)
        x_cord, y_cord = polygon_df['geometry'][0].exterior.coords.xy
        polygon_str = f"({x_cord},{y_cord})"
        metadata = pd.read_csv(self.metadata_path)
        print(metadata.shape)
        # for index, data in enumerate(metadata):
        #         print(index)
        
        # print(metadata.head())
        for index in range(len(metadata)):
                row = metadata.iloc[index]  
                # print(index) 
                # if row['xmin'] <= xmin:
                #         print(True)
                if row['xmin'] <= xmin and row['xmax'] >= xmax and row['ymin'] <= ymin and row['ymax'] >= ymax:
                        region_data = row
                        return bound_tuple , region_data , polygon_str
        return () , {} , ""

    def fetch_file(self):
        with open('assets/pipeline_template.json', 'r') as json_file:
            json_obj = json.load(json_file)

        print(json_obj)
        pipeline = pdal.Pipeline(json.dumps(json_obj)).execute()

        # self.data_count = self.pipeline.execute()

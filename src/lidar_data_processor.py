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
        self.pipline_modifier()
        print(type(self.pipeline['pipeline']))
        pipeline = pdal.Pipeline(json.dumps(self.pipeline))
        pipeline.execute()
        pipeline_array = pipeline.arrays[0]
        return pipeline_array

    def get_geo_df(self, array_data: np.ndarray) -> gpd.GeoDataFrame:
 
        geometry_points = [Point(x, y) for x, y in zip(array_data["X"], array_data["Y"])]
        elevations = array_data["Z"]

        geo_df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
        geo_df['elevation'] = elevations
        geo_df['geometry'] = geometry_points
        geo_df = geo_df.set_geometry("geometry")
        geo_df.set_crs(epsg=self.epsg, inplace=True)
        return geo_df

    def get_region_from_boundary(self):
        polygon_df = gpd.GeoDataFrame([self.polygon], columns=['geometry'])
        polygon_df.set_crs(epsg=self.epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.default_epsg)
        xmin, ymin, xmax, ymax = polygon_df['geometry'][0].bounds
        bound_tuple = (xmin, xmax, ymin, ymax)
        x_cord, y_cord = polygon_df['geometry'][0].exterior.coords.xy
        polygon_str = f"({x_cord},{y_cord})"
        metadata = pd.read_csv(self.metadata_path)
        # print(metadata.shape)
        for index in range(len(metadata)):
                row = metadata.iloc[index]  
                if row['xmin'] <= xmin and row['xmax'] >= xmax and row['ymin'] <= ymin and row['ymax'] >= ymax:
                        region_data = row
                        return bound_tuple , region_data , polygon_str
        return () , {} , ""

    def fetch_file(self):
        pipeline_array = self.pipline_executer()
        self.geo_df = self.get_geo_dep(pipeline_array)
        print(self.geo_df)
        return self.geo_df

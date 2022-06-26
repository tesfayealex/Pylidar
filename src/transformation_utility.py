import numpy as np
import laspy as lp
import geopandas as gpd

class Lidar_Transformation():
    def __init__(self, df : gpd.GeoDataFrame = None, filepath: str= ''):
        """ Initialize lidar transformation class

        Args:
            filepath (String): Filepath of the point cloud data in laz format
         
        Returns:
        None
        """
        if filepath != '':
            self.point_cloud=lp.read(filepath)
            #store coordinates in "points", and colors in "colors" variable
            self.points = np.vstack((self.point_cloud.x, self.point_cloud.y, self.point_cloud.z)).transpose()
        else:
            self.df = df
            self.points = np.vstack((self.df.geometry.x, self.df.geometry.y, self.df.geometry.z)).transpose()




    def decimation(self,points: list=[], factor: int=160):
        """ Sampling with decimation function

        Args:
            points (Dataframe): GeoDataframe of the point cloud data
        Returns:
            list: Decimated points list
        """
        #The decimation strategy, by setting a decimation factor
        if points is []:
            points = self.points
        decimated_points = points[::factor]
        
        return decimated_points


    def grid_subsampling(self,points: list=[], voxel_size: int=6):
        """ Grid subampling of the geodataframe using barycenter grid

        Args:
            points (Dataframe): GeoDataframe of the point cloud data
            voxel_size (Int): voxel size for sub sampling

        Returns:
            list: List of point clouds
        """
        nb_vox=np.ceil((np.max(points, axis=0) - np.min(points, axis=0))/voxel_size)
        non_empty_voxel_keys, inverse, nb_pts_per_voxel= np.unique(((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
        idx_pts_vox_sorted=np.argsort(inverse)
        voxel_grid={}
        grid_barycenter,grid_candidate_center=[],[]
        last_seen=0

        for idx,vox in enumerate(non_empty_voxel_keys):
            voxel_grid[tuple(vox)]=points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
            grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
            grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
            last_seen+=nb_pts_per_voxel[idx]
        return grid_barycenter

if __name__ == "__main__":
    L = Lidar_Transformation()
    L.decimation(L.points)
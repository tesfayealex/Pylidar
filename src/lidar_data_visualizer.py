from asyncore import file_dispatcher
from glob import glob
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import plotting_extent , show_hist


class Lidar_Visualizer():

    def __init__(self , geo_dataframe = None , filepath = None ):
        """ Initializes visualizer class with geodataframe and tiff filepath

        Args:
            geo_dataframe (Dataframe): Geodataframe of the point cloud data.
            filepath (String): Tiff file file path. 

        Returns:
        None
        """
        if geo_dataframe is not None:
            self.geo_dataframe = geo_dataframe
        if filepath is not None:
            self.filepath = filepath
            self.source = rio.open(self.filepath)
    def plot_3d_terrain (self, df=None):
        """ Draws 3d terrain plot of the geodataframe

        Args:
            df (Dataframe): geodataframe of the point cloud data
            
        Returns:
        None
        """
        if df == None:
            df = self.geo_dataframe
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = plt.axes(projection='3d')
        ax.scatter(df.geometry.x, df.geometry.y, df.elevation, s=0.01)
        plt.show()
    def plot_2d_image(self):
        """ Draws 2d image of the raster 

        Args:
        None

        Returns:
        None
        """
        plt.figure(figsize=(10, 6))
        plt.imshow(self.source.read(1), cmap='pink')
        plt.show()
    def plot_geopandas(self):
        """ Draws the raster

        Args:
        None

        Returns:
        None
        """
        plt.figure(figsize=(10, 6))
        rio.plot.show(self.source)
    def plot_image_with_affine_transform(self):
        """ Draws the raster with affine transform 

        Args:
        None

        Returns:
        None
        """
        rio.plot.show((self.source, 1), transform=self.source.transform, cmap='viridis')
    def plot_image_with_contour(self):
        """  Draws the Geodataframe with contour 

        Args:
        None

        Returns:
        None
        """
        fig, ax = plt.subplots(1, figsize=(12, 12))
        rio.plot.show((self.source, 1), ax=ax, contour=True, contour_label_kws={})
    def plot_histogram_of_raster(self):
        """ Draws the histogram of the tiff raster

        Args:
        None

        Returns:
        None
        """
        plt.figure(figsize=(12, 8))
        show_hist(self.source, bins=50, lw=0.0, stacked=False, alpha=0.3,
        histtype='stepfilled', title="Histogram of a raster")
    def plot_grey_rbg_with_histogram(self):
        """ Draws the gray RGB of raster with histogram

        Args:
        None

        Returns:
        None
        """
        fig, (axrgb, axhist) = plt.subplots(1, 2, figsize=(14,7))
        rio.plot.show((self.source), cmap='Greys_r', contour=True, ax=axrgb)
        show_hist(self.source, bins=50, histtype='stepfilled',
                lw=0.0, stacked=False, alpha=0.3, ax=axhist)
        plt.show()
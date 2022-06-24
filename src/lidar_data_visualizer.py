from asyncore import file_dispatcher
from glob import glob
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import plotting_extent , show_hist


class Lidar_Visualizer():

    def __init__(self , geo_dataframe = None , filepath = None ):
        if geo_dataframe is not None:
            self.geo_dataframe = geo_dataframe
        if filepath is not None:
            self.filepath = filepath
            self.source = rio.open(self.filepath)
    def plot_3d_terrain (self, df=None):
        if df == None:
            df = self.geo_dataframe
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = plt.axes(projection='3d')
        ax.scatter(df.geometry.x, df.geometry.y, df.elevation, s=0.01)
        plt.show()
    def plot_2d_image(self):
        plt.figure(figsize=(10, 6))
        plt.imshow(self.source.read(1), cmap='pink')
        plt.show()
    def plot_image_with_affine_transform(self):
        rio.plot.show((self.source, 1), transform=self.source.transform, cmap='viridis')
    def plot_image_with_contour(self):
        fig, ax = plt.subplots(1, figsize=(12, 12))
        rio.plot.show((self.source, 1), ax=ax, contour=True, contour_label_kws={})
    def plot_histogram_of_raster(self):
        plt.figure(figsize=(12, 8))
        show_hist(self.source, bins=50, lw=0.0, stacked=False, alpha=0.3,
        histtype='stepfilled', title="Histogram of a raster")
    def plot_grey_rbg_with_histogram(self):
        fig, (axrgb, axhist) = plt.subplots(1, 2, figsize=(14,7))
        rio.plot.show((self.source), cmap='Greys_r', contour=True, ax=axrgb)
        show_hist(self.source, bins=50, histtype='stepfilled',
                lw=0.0, stacked=False, alpha=0.3, ax=axhist)
        plt.show()
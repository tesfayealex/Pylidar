import re
import json
import requests
import pandas as pd

class Generate_metadata():
    def __init__(self , filename_path: str="" , output_filepath: str= "" , url: str="" , number_of_filename: int= 0):
        """ Initialize metadata generator class with filepaths and number of files

        Args:
            filepath_path (String): path of filename list
            output_filepath (String): path of the metadata csv file to be found 
            url (STring): url of point cloud data location
        Returns:
        None
        """
        self.filename_path = filename_path
        self.output_filepath = output_filepath
        self.number_of_filename = number_of_filename
        self.url = url
    def get_filenames(self):
        """ Filename reader function 

        Args:
        None 

        Returns:
        None
        """
        with open(self.filename_path, "r") as f:
            data = f.read().splitlines()
        self.filenames = data
    def create_metadata_json(self,filename: str= "" , data: json= {}):
        """ create metadata json from data object

        Args:
            filename (String): filename of the region
            data (JSON): full detail data of region 

        Returns:
            JSON: Json data of metadata row
        """
        filename = filename.replace('/','')
        filenames = filename.split('_')
        region = '_'.join(filenames[0:len(filenames)-1])
        year = filenames[-1]
        json_data = {
                        'filename': filename,
                        'region': region,
                        'year': year,
                        'xmin': data['bounds'][0],
                        'xmax': data['bounds'][3],
                        'ymin': data['bounds'][1],
                        'ymax': data['bounds'][4],
                        'zmin': data['bounds'][2],
                        'zmax': data['bounds'][5],
                        'points': data['points'],
                        'version': data['version']

                     }
        
        return json_data
    
    def generate_metadata(self):
        """ Main function which facilitate metadata generation

        Args:
        None

        Returns:
        None
        """
        self.get_filenames()
        metadata = pd.DataFrame(columns=['filename', 'region',
                      'year', 'xmin', 'xmax', 'ymin', 'ymax' , 'zmin' , 'zmax', 'points' , 'version'])
        if self.number_of_filename is None:
                max = len(self.filenames)
        else:
                max = self.number_of_filename

        for file in self.filenames[0:max]:
                        try:
                                result = requests.get(self.url + file + "ept.json")
                                result.raise_for_status()
                                result = result.json()
                                data = self.create_metadata_json(file,result)
                                metadata = metadata.append(data,ignore_index=True)
                        except requests.exceptions.HTTPError as err:
                                pass
        metadata.to_csv(self.output_filepath)

if __name__ == "__main__":
        meta = Generate_metadata('assets/datasource_filenames.txt' , 'assets/metadata.csv', 'https://s3-us-west-2.amazonaws.com/usgs-lidar-public/')
        meta.generate_metadata()

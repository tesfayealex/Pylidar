import re
import json
import requests
import pandas as pd

class Generate_metadata():
    def __init__(self , filename_path , output_filepath , url , number_of_filename = None):
        self.filename_path = filename_path
        self.output_filepath = output_filepath
        self.number_of_filename = number_of_filename
        self.url = url
    def get_filenames(self):
        with open(self.filename_path, "r") as f:
            data = f.read().splitlines()
        self.filenames = data
    def create_metadata_json(self,filename , data):
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
        self.get_filenames()
        metadata = pd.DataFrame(columns=['filename', 'region',
                      'year', 'xmin', 'xmax', 'ymin', 'ymax' , 'zmin' , 'zmax', 'points' , 'version'])
        if self.number_of_filename == None:
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
        metadata.to_csv(self.output_filepath, mode='a')

import re
import json
import requests
import pandas as pd

class Generate_metadata():
    def __init__(self , filename_path , output_filepath , url):
        self.filename_path = filename_path
        self.output_filepath = output_filepath
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

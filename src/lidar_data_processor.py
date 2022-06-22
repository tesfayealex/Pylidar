import pdal
import json


class Lidar_Processor():

    def __init__(self):
        pass
    def fetch_file(self):
        with open('assets/pipeline_template.json', 'r') as json_file:
            json_obj = json.load(json_file)

        print(json_obj)
        pipeline = pdal.Pipeline(json.dumps(json_obj)).execute()

        # self.data_count = self.pipeline.execute()

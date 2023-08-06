import json
import os
import sys


class __Config:

    def __init__(self):
        self.api_url = 'https://api.instabuy.com.br'
        self.items_batch_count = 1000
        self.program_path: str = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.ib_integration_temp_files = os.path.join(self.program_path, 'tmp')
        self.version_file_name: str = "version.txt"
        self.DEBUG = False

    def get_local_version(self):
        local_vpath = os.path.join(self.program_path, self.version_file_name)

        if not os.path.exists(local_vpath):
            return None

        local_version = ''
        with open(local_vpath, "r", encoding='utf-8') as local_vfile:
            local_version = local_vfile.read()

        return local_version

    def load_local_config(self, local_file_name="config.json"):
        with open(os.path.join(self.program_path, local_file_name), 'r') as local_file:
            local_config = (json.load(local_file))

            for key in local_config:
                self.__setattr__(key, local_config[key])


config = __Config()

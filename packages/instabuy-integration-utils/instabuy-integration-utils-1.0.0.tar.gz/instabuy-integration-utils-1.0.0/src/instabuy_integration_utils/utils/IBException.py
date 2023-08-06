import datetime
import os
import traceback
import requests
from instabuy_integration_utils.config import config
from instabuy_integration_utils.update import IBSelfUpdate


class IBException:

    @staticmethod
    def save_exception(exception):
        
        try:
            robot_name = config.get("robot_name")
        except AttributeError:
            robot_name = "generic"

        data = {
            'error': str(exception),
            'created_at': datetime.datetime.utcnow(),
            'robot': robot_name,
            'version': IBSelfUpdate.get_local_version(),
            'traceback': traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__)
        }

        response = requests.post(f'{config.api_url}/api_py_robots/errors', data=data)
        if response.status_code != 200:
            with open(os.path.join(config.program_path, 'log_errors.txt'), 'a+', encoding='utf-8') as my_file:
                my_file.write('\n\n\n' + ''.ljust(70, '*') + '\n')
                my_file.write(str(data))
                my_file.write('\n' + ''.ljust(70, '*') + '\n')

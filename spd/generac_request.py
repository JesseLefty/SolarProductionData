import requests
import json
import os

DVCS_MAP = {
    'NAME': 'n',
    'IDS': 's',
    'STATE': 'st',
    'POWER': 'p',
    'TOTAL_ENERGY': 'et',
    'UPDATE': 'up'
}


def save_data(data: dict, file_path: str, file_name: str):
    output_json = json.dumps(data, indent=4)
    path = os.path.join(file_path, file_name + '.json')
    with open(path, 'w') as file:
        file.write(output_json)


class DashboardInfo:

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.devices = requests.get(self.url, headers=self.headers).json()
        self.device_info = {}

    def device_information(self, info, search_criteria=None, request_list=None):
        if request_list is None and search_criteria is None:
            self.device_info[info] = [i[DVCS_MAP[info]] for i in self.devices['dvcs']]
        else:
            request_list = [str(i) for i in request_list]
            self.device_info[info] = [i[DVCS_MAP[info]] for i in self.devices['dvcs'] if
                                      i[DVCS_MAP[search_criteria]] in request_list]

        return self.device_info[info]

    def save_file(self, file_path: str, file_name: str):
        save_data(self.devices, file_path, file_name)


class Data:

    def __init__(self, device_id):
        self.device_id = device_id

    def power(self):
        pass

    def energy(self):
        pass

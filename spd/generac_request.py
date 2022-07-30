import requests


DVCS_MAP = {
            'NAME': 'n',
            'IDS': 's',
            'STATE': 'st'
            }


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

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
        self.device_ids = []
        self.device_names = []
        self.device_state = []

    def _clear(self):
        self.device_ids = []
        self.device_names = []
        self.device_state = []
        self.device_info = {
                            'IDS': self.device_ids,
                            'NAME': self.device_names,
                            'STATE': self.device_state
                            }

    def device_information(self, info, search_criteria=None, request_list=None):
        self._clear()
        if request_list is None and search_criteria is None:
            self.device_info['IDS'] = [i[DVCS_MAP['IDS']] for i in self.devices['dvcs']]
            self.device_info['NAME'] = [i[DVCS_MAP['NAME']] for i in self.devices['dvcs']]
            self.device_info['STATE'] = [i[DVCS_MAP['STATE']] for i in self.devices['dvcs']]
        else:
            request_list = [str(i) for i in request_list]
            for item in self.devices['dvcs']:
                if item[DVCS_MAP[search_criteria]] in request_list:
                    self.device_info['IDS'].append(item[DVCS_MAP['IDS']])
                    self.device_info['NAME'].append(item[DVCS_MAP['NAME']])
                    self.device_info['STATE'].append(item[DVCS_MAP['STATE']])
        return self.device_info[info]

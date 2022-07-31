"""
This module is contains the methods and classes for requesting .json data from the Pwrcell.Generac.com web site.
"""
import requests
import json
import os

DVCS_MAP = {
    'NAME': 'n',
    'IDS': 's',
    'STATE': 'st',
    'POWER': 'p',
    'TOTAL_ENERGY': 'et',
    'UPDATE_TIME': 'up'
}


def save_data(data: dict, file_path: str, file_name: str):
    """
    Saves data in the form of a JSON file

    :param data:        Data to save to a JSON file
    :param file_path:   File path to the desired save location
    :param file_name:   Name of saved file

    :return:            None
    """
    output_json = json.dumps(data, indent=4)
    path = os.path.join(file_path, file_name + '.json')
    with open(path, 'w') as file:
        file.write(output_json)


def build_cookie(remember_token: str, session_cookie=''):
    """
    Builds the cookie information required to access the Generac Request URL. If a session cookie is not provided
    the cookie will be automatically extracted from the base pwrcell website headers. A remember token is ALWAYS
    required

    :param remember_token:  authorization token stored in web browser use to validate user authentication. This token
                            can be located by navigating to the pwrcell.generac.com user dashboard, using the web
                            inspection tool network tab and selecting 'dashboard'. The remember token is located in the
                            Request Headers at the end of 'Cookie'
    :param session_cookie:  web browser cookie value for pwrcell.generac.com. When provided, this cookie should NOT
                            include the 'name' parameter

    :return:                Returns the cookie in the format requested by the Generac URL.
    """
    if not session_cookie:
        content = requests.get('https://pwrcell.generac.com')
        cookie = content.headers['Set-Cookie'].split(";")[0] + '; remember_token=' + remember_token
    else:
        cookie = session_cookie + '; remember_token=' + remember_token
    return cookie


class DashboardInfo:

    def __init__(self, url, header):
        self.url = url
        self.headers = header
        self.devices = requests.get(self.url, headers=self.headers).json()
        self.device_info = {}

    def device_information(self, info, search_criteria=None, request_list=None) -> list:
        """
        Populates the solar installation device information dictionary with device values based on user search criteria
        and a request list. If a search criteria and request list is not provided, the information for all devices is
        returned

        Valid information and shear criteria is contained in the following dictionary.

            'NAME': 'n',
            'IDS': 's',
            'STATE': 'st',
            'POWER': 'p',
            'TOTAL_ENERGY': 'et',
            'UPDATE_TIME': 'up'

        :param info:                Requested device information (see above dictionary)
        :param search_criteria:     Criteria for which the request list should be searched
        :param request_list:        List of specific device values for which the requested info should be returned.

        :return                     None

        example:
            To return a list of total energy ('et') produced by devices with the name 'PV Link' and 'PWRcell Inverter'
            this method would be run with the parameters (info='TOTAL_ENERGY', search_criteria='NAME',
                                                            request_list=['PV Link, 'PWRcell Inverter])
        """
        if request_list is None and search_criteria is None:
            self.device_info[info] = [i[DVCS_MAP[info]] for i in self.devices['dvcs']]
        else:
            request_list = [str(i) for i in request_list]
            self.device_info[info] = [i[DVCS_MAP[info]] for i in self.devices['dvcs'] if
                                      i[DVCS_MAP[search_criteria]] in request_list]

        return self.device_info[info]

    def save_file(self, file_path: str, file_name: str):
        """
        saves the device list and all values as a JSON file

        :param file_path:   File path to the desired save location
        :param file_name:   Name of saved file

        :return: None
        """
        save_data(self.devices, file_path, file_name)


class DeviceData:

    def __init__(self, device_id: str, headers: dict):
        self.device_id = device_id
        self.headers = headers
        self.data = {}

    def power_data(self):
        """
        returns the power data as a dictionary for the specific device id associated with the DeviceData object
        """
        url = 'https://pwrcell.generac.com/power/{}/now/all.json'.format(f'{self.device_id}')
        self.data = requests.get(url, headers=self.headers).json()
        return self.data

    def energy_data(self):
        """
        returns the energy data as a dictionary for the specific device id associated with the DeviceData object
        """
        url = 'https://pwrcell.generac.com/energy/{}/now/all.json'.format(f'{self.device_id}')
        self.data = requests.get(url, headers=self.headers).json()
        return self.data

    def save_file(self, file_path: str, file_name: str):
        """
        saves the device list and all values as a JSON file

        :param file_path:   File path to the desired save location
        :param file_name:   Name of saved file

        :return: None
        """
        save_data(self.data, file_path, file_name)

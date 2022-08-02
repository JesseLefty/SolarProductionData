import time
import json


def date_to_epoch(date: str, hour: int = 0):
    complete_date = f'{date}: {str(hour)}'
    pattern = '%m-%d-%Y: %H'
    return int(time.mktime(time.strptime(complete_date, pattern)))

#todo: provide corresponding date and time with max / min
#todo: figure out how class inheritance works


class ProductionData:

    def __init__(self, data: list[list],
                 begin_date: str = '',
                 end_date: str = '',
                 begin_hour: int = 0,
                 end_hour: int = 0):

        self.data = data
        if begin_date == '':
            self.begin_time = 0
        else:
            self.begin_time = date_to_epoch(begin_date, begin_hour)
        if end_date == '':
            self.end_time = time.mktime(time.localtime())
        else:
            self.end_time = date_to_epoch(end_date, end_hour)
        self.zero_list = [None]
        self.data_in_range = self.production_in_range()

    def count_zero(self):
        return len([i for i in self.data_in_range if i[1] <= 0])

    def get_zero(self):
        self.zero_list = [i for i in self.data_in_range if i[1] >= 0]
        return self.zero_list

    def production_in_range(self):
        return [i for i in self.data if self.begin_time <= i[0]/1000 < self.end_time]

    def max(self):
        return max([i[1] for i in self.data_in_range])

    def min(self):
        return min([i[1] for i in self.data_in_range])

    def all_data(self, zeros=False):
        pass

    def daily(self, zeros=False):
        pass


class Power(ProductionData):
    def __init__(self, data: list[list]):
        super().__init__(data)


print(date_to_epoch('07-20-2022'))
with open(r'C:\Users\Jesse\Desktop\Solar Data\power test.json', 'r') as f:
    data = json.load(f)
power_data = data['wh_per_hour']

power = ProductionData(power_data, begin_date='05-10-2021', end_date='7-12-2022')

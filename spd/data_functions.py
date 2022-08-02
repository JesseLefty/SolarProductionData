import time
import json


def date_to_epoch(date: str, hour: int = 0):
    complete_date = f'{date}: {str(hour)}'
    pattern = '%m-%d-%Y: %H'
    return int(time.mktime(time.strptime(complete_date, pattern)))


def epoch_to_date(date: int):
    return time.strftime("%d %b %Y %H:%M:%S", time.gmtime(date))




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
        self.data_in_range = self._production_in_range()
        self.time = [i[0] for i in self.data_in_range]
        self.production = [i[1] for i in self.data_in_range]
        self.bool = [i[2] for i in self.data_in_range]

    def count_zero(self):
        return len([i for i in self.production if i <= 0])

    def get_zero(self):
        self.zero_list = [i for i in self.data_in_range if i[1] >= 0]
        return self.zero_list

    def _production_in_range(self):
        return [i for i in self.data if self.begin_time*1000 <= i[0] < self.end_time*1000]

    def max(self, with_date=False, epoch=True):
        max_val = max([i for i in self.production])
        if not with_date:
            return max_val
        else:
            max_index = self.production.index(max_val)
            date = self.time[max_index]
            if not epoch:
                date = epoch_to_date(date)
            return [date, max_val]
#todo: fix the epoch_to_date conversion

    def min(self, with_date=False, epoch=True):
        min_val = min([i for i in self.production])
        if not with_date:
            return min_val
        else:
            min_index = self.production.index(min_val)
            date = self.time[min_index]
            if not epoch:
                date = epoch_to_date(date)
            return [date, min_val]

    def all_data(self, zeros=False, epoch=True):
        data_dict = {'Range': [self.begin_time, self.end_time],
                     'Max': self.max(with_date=True, epoch=epoch),
                     'Min': self.min(with_date=True, epoch=epoch),
                     'No Production': self.count_zero()}
        if not epoch:
            data_dict['Range'] = [epoch_to_date(self.begin_time), epoch_to_date(self.end_time)]
        return data_dict

    def daily(self, zeros=False):
        pass

    def match_date(self, value: int):
        pass


class Power(ProductionData):
    def __init__(self, data: list[list]):
        super().__init__(data)


with open(r'C:\Users\Jesse\Desktop\Solar Data\power test.json', 'r') as f:
    data = json.load(f)
power_data = data['wh_per_hour']

power = ProductionData(power_data, begin_date='05-10-2021', end_date='7-12-2022')
print(power.max())
print(power.all_data(epoch=False))
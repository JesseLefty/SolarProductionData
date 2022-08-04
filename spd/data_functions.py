from datetime import datetime, timedelta
import time
import json

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def date_to_epoch(date: str):
    return int(time.mktime(time.strptime(date, DATE_FORMAT)))


class ProductionData:

    def __init__(self, data: list[list],
                 begin_date: str = '',
                 end_date: str = ''):

        self.data = data
        self.begin_time = begin_date
        self.end_time = end_date
        self.zero_list = [None]
        self.time = [datetime.fromtimestamp(t[0] // 1000).strftime(DATE_FORMAT) for t in self.data]
        self.production = [i[1] for i in self.data]
        self.bool = [i[2] for i in self.data]
        self.data_in_range = self._production_in_range()
        self.time_in_range = [datetime.fromtimestamp(t[0] // 1000).strftime(DATE_FORMAT) for t in self.data_in_range]
        self.production_in_range = [i[1] for i in self.data_in_range]
        self.bool_in_range = [i[2] for i in self.data_in_range]
        self.start_date_list = self.begin_time.split('-')
        self.end_date_list = self.end_time.split('-')

    def count_zero(self):
        return len([i for i in self.production if i <= 0])

    def get_zero(self):
        self.zero_list = [i for i in self.data_in_range if i[1] >= 0]
        return self.zero_list

    def _production_in_range(self):
        begin_date = date_to_epoch(self.begin_time)
        end_date = date_to_epoch(self.end_time)
        return [item for idx, item in enumerate(self.data) if begin_date <= date_to_epoch(self.time[idx]) <= end_date]

    def max(self, with_date=False):
        max_val = max([i for i in self.production_in_range])
        if not with_date:
            return max_val
        else:
            max_index = self.production_in_range.index(max_val)
            date = self.time_in_range[max_index]
            return [date, max_val]

    def min(self, with_date=False):
        min_val = min([i for i in self.production_in_range])
        if not with_date:
            return min_val
        else:
            min_index = self.production_in_range.index(min_val)
            date = self.time_in_range[min_index]
            return [date, min_val]

    def all_data(self):
        data_dict = {'Range': [self.begin_time, self.end_time],
                     'Max': self.max(with_date=True),
                     'Min': self.min(with_date=True),
                     'No Production': self.count_zero()}
        return data_dict

    def group_by_day(self):
        start = datetime.strptime(self.begin_time.split(" ")[0], "%Y-%m-%d")
        end = datetime.strptime(self.end_time.split(" ")[0], "%Y-%m-%d")
        date_generated = [start + timedelta(days=x) for x in range(0, (end - start).days)]
        days = {}
        for date in date_generated:
            day_list = []
            for index, item in enumerate(self.time_in_range):
                time_as_list = item.split('-')
                year = int(time_as_list[0])
                month = int(time_as_list[1])
                day = int(time_as_list[2].split(" ")[0])
                if datetime(year=year, month=month, day=day) > date:
                    break
                if datetime(year=year, month=month, day=day) == date:
                    day_list.append(self.production_in_range[index])
            days[datetime.strftime(date, DATE_FORMAT)] = day_list
        return days

    def match_date(self, value: int):
        pass


class Power(ProductionData):
    def __init__(self, data: list[list]):
        super().__init__(data)


with open(r'C:\Users\Jesse\Desktop\Solar Data\power test.json', 'r') as f:
    data = json.load(f)
power_data = data['wh_per_hour']

power = ProductionData(power_data, begin_date='2022-06-10 20:00:00', end_date='2022-07-12 10:00:00')
print(power.group_by_day())



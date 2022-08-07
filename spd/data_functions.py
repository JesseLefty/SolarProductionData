from datetime import datetime, timedelta
import time

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def date_to_epoch(date: str):
    return int(time.mktime(time.strptime(date, DATE_FORMAT)))


class Power:

    def __init__(self, data: list[list],
                 begin_date: str,
                 end_date: str):
        self.data = data
        self.time = [datetime.fromtimestamp(t[0] // 1000).strftime(DATE_FORMAT) for t in self.data]
        self.begin_time = begin_date
        self.end_time = end_date

        if not self._check_valid_dates():
            raise ValueError

        self.production = [i[1] for i in self.data]
        self.bool = [i[2] for i in self.data]
        self.zero_list = [None]
        self.data_in_range = self._production_in_range()
        self.time_in_range = [datetime.fromtimestamp(t[0] // 1000).strftime(DATE_FORMAT) for t in self.data_in_range]
        self.production_in_range = [i[1] for i in self.data_in_range]
        self.bool_in_range = [i[2] for i in self.data_in_range]
        self.start_date_list = self.begin_time.split('-')
        self.end_date_list = self.end_time.split('-')

    def _check_valid_dates(self):
        if self.time[0] > self.begin_time:
            print(f'begin date cannot be earlier than {self.time[0]}')
            return False
        elif self.time[-1] < self.end_time:
            print(f'end date cannot be later than {self.time[-1]}')
        elif self.end_time <= self.begin_time:
            print(f'end date cannot be before or equal to the begin date')
        else:
            return True

    def _production_in_range(self):
        begin_date = date_to_epoch(self.begin_time)
        end_date = date_to_epoch(self.end_time)
        return [item for idx, item in enumerate(self.data) if begin_date <= date_to_epoch(self.time[idx]) <= end_date]

    @staticmethod
    def _average(power_data: list, date_data: list, n: int = 1, precision: int = 2):
        i = 0
        result = {}
        while i < len(power_data) - n + 1:
            power_window = power_data[i:i + n]
            date_window = date_data[i:i + n]
            window_average = round(sum(power_window) / n, precision)
            result[(date_window[0], date_window[-1])] = window_average
            i += 1

        return result

    def count_zero(self):
        return len([i for i in self.production if i <= 0])

    def get_zero(self):
        self.zero_list = [i for i in self.data_in_range if i[1] >= 0]
        return self.zero_list

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

    def hourly_average(self, n: int = 1, precision: int = 1):
        return self._average(self.production_in_range, self.data_in_range, n=n, precision=precision)

    def daily_average(self, n: int = 1, precision: int = 1):
        daily_data = self.group_by_day()
        daily_production = [sum(v) for v in daily_data.values()]
        daily_dates = [k for k in daily_data.keys()]
        return self._average(daily_production, daily_dates, n=n, precision=precision)

    def weekly_average(self):
        pass

    def monthly_average(self):
        pass

    def yearly_average(self):
        pass

    def all_data(self):
        data_dict = {'Range': [self.begin_time, self.end_time],
                     'Max': {'Hour': self.max(with_date=True),
                             'Day': 'WIP'},
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

    def group_by_week(self):
        pass

    def group_by_month(self):
        pass

    def group_by_year(self):
        pass

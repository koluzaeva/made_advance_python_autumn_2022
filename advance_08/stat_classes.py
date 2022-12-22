'''statistic classes'''

import time
from typing import Union, Dict

Number = Union[int, float, complex]


class BaseMetric:
    '''BaseMetric class'''
    def __init__(self, name: str):
        self.__name__ = name

    def get_name(self):
        return self.name

    def get_value(self):
        pass

    def add(self, value: Number):
        pass

    def clear(self):
        pass


class MetricTimer(BaseMetric):
    '''MetricTimer class'''
    def __init__(self, name: str):
        super().__init__(name)
        self.proc_time: Number
        self.start = 0
        self.proc_time = 0

    def add(self):
        self.proc_time = time.time() - self.start

    def get_value(self):
        return self.proc_time

    def clear(self):
        self.proc_time = 0
        self.start = 0

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_value, tb):
        self.proc_time = time.time() - self.start




class MetricAvg(BaseMetric):
    '''MetricAvg class'''
    def __init__(self, name: str):
        super().__init__(name)
        self.value: Number
        self.count = 0
        self.value = 0

    def add(self, value: Number):
        self.value += value
        self.count += 1

    def get_value(self):
        return self.value / self.count

    def clear(self):
        self.count = 0
        self.value = 0


class MetricCount(BaseMetric):
    '''MetricCount class'''
    def __init__(self, name: str):
        super().__init__(name)
        self.count = 0

    def add(self):
        self.count += 1

    def get_value(self):
        return self.count

    def clear(self):
        self.count = 0


MetricClass = Union[MetricTimer, MetricAvg, MetricCount]


class Stats:
    '''Stats class'''
    timer_stat: Dict[str, MetricClass]
    avg_stat: Dict[str, MetricClass]
    count_stat: Dict[str, MetricClass]
    timer_stat = {}
    avg_stat = {}
    count_stat = {}

    @classmethod
    def timer(cls, name: str):
        if not cls.timer_stat.get(name):
            cls.timer_stat[name] = MetricTimer(name)
        return cls.timer_stat[name]

    @classmethod
    def avg(cls, name: str):
        if not cls.avg_stat.get(name):
            cls.avg_stat[name] = MetricAvg(name)
        return cls.avg_stat[name]

    @classmethod
    def count(cls, name: str):
        if not cls.count_stat.get(name):
            cls.count_stat[name] = MetricCount(name)
        return cls.count_stat[name]

    @classmethod
    def collect(cls):
        cls_func = ['timer', 'avg', 'count']
        func_stat = {}
        for i, metrics in enumerate([cls.timer_stat, cls.avg_stat, cls.count_stat]):
            for key in metrics.keys():
                if metrics[key].get_value() != 0:
                    func_stat[f'{key}.{cls_func[i]}'] = metrics[key].get_value()
            metrics.clear()

        return func_stat


def calc():
    i = 0
    for _ in range(100000):
        i += 1
    return 3


with Stats.timer("calc"):  # 0.1
    res = calc()  # 3

Stats.count("calc").add()
Stats.avg("calc").add(res)

Stats.timer("calc").add()  # 0.005
Stats.count("calc").add()
Stats.avg("calc").add(res)

Stats.count("http_get_data").add()
Stats.avg("http_get_data").add(0.7)

Stats.count("no_used")  # не попадет в результат collect

metrics = Stats.collect()
print(metrics)

metrics = Stats.collect()
print(metrics)
assert metrics == {}

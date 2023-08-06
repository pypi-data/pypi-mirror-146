import time


class Aggregator:
    def aggregate(self, values):
        raise NotImplemented()


class SumAggregator:
    def aggregate(self, values):
        return sum(values)


class AvgAggregator:
    def aggregate(self, values):
        if not values:
            return 0
        else:
            return sum(values) / len(values)

class RateAggregator:
    def __init__(self):
        self.window_start_ts = time.time()

    def aggregate(self, values):
        window_end_ts = time.time()

        res = sum(values) / (window_end_ts - self.window_start_ts)

        self.window_start_ts = window_end_ts
        return res

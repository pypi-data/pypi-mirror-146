from abc import ABC, abstractmethod
import pprint
import statistics


class SorterBase(ABC):
    def __init__(self, objects=None, key_func=lambda _: _, values=None, deviation_point=None):
        self.__objects = [_ for _ in objects] if objects is not None else None
        self.__values = [_ for _ in values] if values is not None else None
        if key_func is not None:
            self.key_func = key_func
        if deviation_point is not None:
            self.deviation_point = deviation_point

    @property
    def objects(self):
        return self.__objects

    def __clean__(self):
        attrs_to_delete = ['sorted', 'deviations', 'abs_deviations', 'avg_deviation',
                           'abs_avg_deviation',
                           'pstdev', 'deviation_rates', 'abs_deviation_rates']
        for _ in attrs_to_delete:
            if hasattr(self, _):
                delattr(self, _)

    @objects.setter
    def objects(self, value):
        self.__clean__()
        self.__objects = value
        self.__values = None
        if self.get_deviation_point() is None:
            delattr(self, 'deviation_point')

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, value):
        self.__clean__()
        self.__values = value
        if self.get_deviation_point() is None:
            delattr(self, 'deviation_point')

    def get_values(self):
        if self.values is not None:
            return self.values
        if not hasattr(self, 'key_func'):
            self.values = []
            return self.values
        self.values = [self.key_func(_) for _ in self.objects]
        return self.values

    def get_sorted(self):
        if hasattr(self, 'sorted'):
            return self.sorted
        if self.objects is None:
            self.sorted = []
            return []
        self.sorted = [i[0] for i in sorted(zip(self.objects, self.get_abs_deviations()), key=lambda _: _[1])]
        return self.sorted

    def get_deviation_point(self):
        if hasattr(self, 'deviation_point'):
            return self.deviation_point
        values = self.get_values()
        if not values:
            self.deviation_point = None
            return self.deviation_point
        self.deviation_point = self.calculate_deviation_point()
        return self.deviation_point

    @abstractmethod
    def calculate_deviation_point(self):
        pass

    def get_deviations(self):
        if hasattr(self, 'deviations'):
            return self.deviations
        deviation_point = self.get_deviation_point()
        self.deviations = [_ - deviation_point for _ in self.get_values()]
        return self.deviations

    def get_abs_deviations(self):
        if hasattr(self, 'abs_deviations'):
            return self.abs_deviations
        self.abs_deviations = [abs(i) for i in self.get_deviations()]
        return self.abs_deviations

    def get_avg_deviation(self):
        if hasattr(self, 'avg_deviation'):
            return self.avg_deviation
        deviations = self.get_deviations()
        if not deviations:
            self.avg_deviation = None
            return self.avg_deviation
        self.avg_deviation = sum(deviations) / len(deviations)
        return self.avg_deviation

    def get_abs_avg_deviation(self):
        if hasattr(self, 'abs_avg_deviation'):
            return self.abs_avg_deviation
        abs_deviations = self.get_abs_deviations()
        if not abs_deviations:
            self.abs_avg_deviation = None
            return self.abs_avg_deviation
        self.abs_avg_deviation = sum(abs_deviations) / len(abs_deviations)
        return self.abs_avg_deviation

    def get_pstdev(self):
        if hasattr(self, 'pstdev'):
            return self.pstdev
        values = self.get_values()
        if not values:
            self.pstdev = None
            return self.pstdev
        self.pstdev = statistics.pstdev(self.get_values())
        return self.pstdev

    def get_deviation_rates(self):
        if hasattr(self, 'deviation_rates'):
            return self.deviation_rates
        deviations = self.get_deviations()
        abs_avg_deviation = self.get_abs_avg_deviation()
        self.deviation_rates = [i / abs_avg_deviation if abs_avg_deviation != 0 else 0 for i in
                                deviations]
        return self.deviation_rates

    def get_abs_deviation_rates(self):
        if hasattr(self, 'abs_deviation_rates'):
            return self.abs_deviation_rates
        self.abs_deviation_rates = [abs(i) for i in self.get_deviation_rates()]
        return self.abs_deviation_rates

    def __repr__(self):
        return '\n' + 'Values: ' + pprint.pformat(
            self.get_values()) + '\n' + 'Objects: ' + pprint.pformat(
            self.objects if hasattr(self, 'objects') else []) + '\n' + 'Get sorted: ' + pprint.pformat(
            self.get_sorted()) + '\n' + 'Deviation point: ' + pprint.pformat(
            self.get_deviation_point()) + '\n' + 'Deviations: ' + pprint.pformat(
            self.get_deviations()) + '\n' + 'Abs deviations: ' + pprint.pformat(
            self.get_abs_deviations()) + '\n' + 'Avg deviation: ' + pprint.pformat(
            self.get_avg_deviation()) + '\n' + 'Abs avg deviation: ' + pprint.pformat(
            self.get_abs_avg_deviation()) + '\n' + 'Pstdev: ' + pprint.pformat(
            self.get_pstdev()) + '\n' + 'Deviation rates: ' + pprint.pformat(
            self.get_deviation_rates()) + '\n' + 'Abs deviation rates: ' + pprint.pformat(
            self.get_abs_deviation_rates()) + '\n'


class MinSorter(SorterBase):
    def calculate_deviation_point(self):
        return min(self.get_values())


class MaxSorter(SorterBase):
    def calculate_deviation_point(self):
        return max(self.get_values())


class MedianSorter(SorterBase):
    def calculate_deviation_point(self):
        values = self.get_values()
        return statistics.median(values)


class MeanSorter(SorterBase):
    def calculate_deviation_point(self):
        values = self.get_values()
        return statistics.mean(values)


def get_multi_sorted(objects, sorters):
    if not objects:
        return []
    abs_deviation_rates = [0 for _ in objects]
    for sorter in sorters:
        if sorter.objects is None:
            sorter.objects = objects
        for index, value in enumerate(sorter.get_abs_deviation_rates()):
            abs_deviation_rates[index] += value
    return [i[0] for i in sorted(zip(objects, abs_deviation_rates), key=lambda _: _[1])]



from typing import Callable

import pandas as pd


class AbstractMetric:
    def compute(self, data: pd.DataFrame):
        ...


class FilteredMetric(AbstractMetric):
    def __init__(self, applied_metric: AbstractMetric, filtering_fn: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        super().__init__()
        self.applied_metric: AbstractMetric = applied_metric
        self.filtering_fn: Callable[[pd.DataFrame], pd.DataFrame] = filtering_fn

    def compute(self, data: pd.DataFrame):
        filtered_data: pd.DataFrame = self.filtering_fn(data)
        return self.applied_metric(filtered_data)


def bv_filtering_building(bv_num: int) -> Callable[[pd.DataFrame], pd.DataFrame]:
    def bv_filtering(data: pd.DataFrame) -> pd.DataFrame:
        return data[data.bv == bv_num]
    return bv_filtering


def bv_filtering_building(bv_num: int) -> Callable[[pd.DataFrame], pd.DataFrame]:
    def bv_filtering(data: pd.DataFrame) -> pd.DataFrame:
        return data[data.bv == bv_num]
    return bv_filtering


class GroupedMetric(AbstractMetric):
    def __init__(self, group_by_condition: str, fn: Callable) -> None:
        super().__init__()
        self.group_by_condition: str = group_by_condition
        self.fn: Callable = fn

    def compute(self, data: pd.DataFrame):
        return data.groupby(self.group_by_condition).apply(self.fn)

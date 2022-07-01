import json
from typing import Dict, List, Optional

import pandas as pd

from bvinterpreter.viz.metrics import AbstractMetric, GroupedMetric


class MapDataCreator:
    def __init__(self, address_info: pd.DataFrame, metrics: Dict[str, AbstractMetric]) -> None:
        self.address_info: pd.DataFrame = address_info
        self.metrics: Dict[str, AbstractMetric] = metrics
        self.col_rename: Dict[str, str] = {"bv": "Identifiant du bureau de vote"}

    def create(self, data: pd.DataFrame):
        results: Dict = {}
        for key, m in self.metrics.items():
            results[key] = m.compute(data)
        mapping_data: Dict = self.aggregate(results)
        return mapping_data

    def generate(self, data_path: str, path_out: str):
        """Generate the metrics and write them to disk

        Args:
            data_path (str): The data to read
            path_out (str): The data path to write the result to

        Examples:
            >>> import os
            >>> bv_info_path: Optional[str] = os.getenv("BV_INFO_PATH", os.path.join("data", "raw", "bv_list.csv"))
            >>> address_info: pd.DataFrame = pd.read_csv(bv_info_path)
            >>> metrics: Dict[str, AbstractMetric] = {
            ...     "Total vote 1er tour": GroupedMetric("bv", lambda x: x.vote_01.sum()),
            ...     "Total vote 2eme tour": GroupedMetric("bv", lambda x: x.vote_02.sum()),
            ...     "Retour second tour": GroupedMetric("bv", lambda x: x[x.vote_01 == 1].vote_02.sum()),
            ...     "Seulement 2eme tour": GroupedMetric("bv", lambda x: x[x.vote_01 == 0].vote_02.sum()),
            ...     "Seulement 1er tour": GroupedMetric("bv", lambda x: x[x.vote_02 == 0].vote_01.sum()),
            ...     "Procuration 1er tour": GroupedMetric("bv", lambda x: x.proc_01.sum()),
            ...     "Procuration 2eme tour": GroupedMetric("bv", lambda x: x.proc_02.sum()),
            ... }
            >>> obj: MapDataCreator = MapDataCreator(address_info=address_info, metrics=metrics)
            >>> path_in: str = os.path.join("tests", "resources", "test.csv")
            >>> path_out: str = os.path.join("tests", "map_creation_result.csv")
            >>> obj.generate(path_in, path_out)
        """
        data: pd.DataFrame = pd.read_csv(data_path)
        self.create(data=data)
        self.address_info.to_csv(path_out)

    def aggregate(self, results: Dict[str, pd.DataFrame]):
        for key, df in results.items():
            self.address_info = self.address_info.merge(df.to_frame(name=key).reset_index().rename(columns=self.col_rename))


if __name__ == "__main__":
    import fire
    import os
    bv_info_path: Optional[str] = os.getenv("BV_INFO_PATH", os.path.join("data", "raw", "bv_list.csv"))
    bv_info: pd.DataFrame = pd.DataFrame()
    metrics: List[AbstractMetric] = [GroupedMetric("")]
    obj: MapDataCreator = MapDataCreator(bv_info=bv_info, metrics=metrics)
    fire.Fire(obj)

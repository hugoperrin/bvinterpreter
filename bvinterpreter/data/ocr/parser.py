from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass()
class VotingData:
    address: str = ""
    name: str = ""
    proc: bool = False
    first: bool = False
    second: bool = False
    n_elec: int = -1


class AbstractParser:
    def parse(self, data: pd.DataFrame) -> pd.DataFrame:
        ...


class BaseParser(AbstractParser):
    def parse_line(self, line: List[str]) -> VotingData:
        ## Here the issue is on line parsing, as the tesseract ocr seems to perform rather poorly and not adequately to signatures
        return VotingData()

    def parse(self, data: Dict) -> pd.DataFrame:
        parsed_data: Dict[str, List] = {
            "n_elec": [],
            "name": [],
            "proc": [],
            "signed_1st": [],
            "signed_2nd": [],
            "address": [],
            "bv": [],
        }
        line_data: List[List[str]] = [[]]
        for line_num, text in zip(data["line_num"], data["text"]):
            if len(text) == 0:
                continue
            if line_num == len(line_data):
                line_data.append([])
            line_data[line_num].append(text)
        bv_num: int = -1
        for line in line_data[-25:]:
            parsed_line: VotingData = self.parse_line(line)
            parsed_data["address"].append(parsed_line.address)
            parsed_data["name"].append(parsed_line.name)
            parsed_data["proc"].append(parsed_line.proc)
            parsed_data["signed_1st"].append(parsed_line.first)
            parsed_data["signed_2nd"].append(parsed_line.second)
            parsed_data["n_elec"].append(parsed_line.n_elec)
            parsed_data["bv"].append(bv_num)
        return pd.DataFrame.from_dict(parsed_data)

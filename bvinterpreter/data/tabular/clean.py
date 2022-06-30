from typing import List, Optional

import pandas as pd


def merge(ocr_files: List[str]) -> pd.DataFrame:
    df: Optional[pd.DataFrame] = None
    for path in ocr_files:
        read_df: pd.DataFrame = pd.read_csv(path)
        if df is None:
            df = read_df
        else:
            df = df.join(read_df)

    return df

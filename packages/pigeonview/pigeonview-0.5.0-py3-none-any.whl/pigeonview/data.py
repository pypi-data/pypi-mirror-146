"""
Data utilities.
"""
from typing import Any, Dict, Optional, Union

import pandas as pd  # type: ignore


def resample_df(
        df: pd.DataFrame,
        timestamp_col: str,
        interval: str = "1D",
        default_aggregation_method: str = "mean",
        aggregation_methods: Optional[Dict[str, str]] = None,
        **kwargs: Any
) -> pd.DataFrame:
    if aggregation_methods is None:
        aggregation: Union[str, Dict[str, str]] = default_aggregation_method
    else:
        aggregation = dict(zip(
            df.columns, [default_aggregation_method] * len(df.columns)
        ))
        aggregation.update(aggregation_methods)
    return df.resample(interval, on=timestamp_col, **kwargs).agg(aggregation)

"""
Data utilities.
"""
from datetime import datetime
from typing import Dict, Optional, Union

import pandas as pd  # type: ignore

from pigeonview.persistence import PersistenceBase


def _resample_df(
        df: pd.DataFrame,
        timestamp_col: str,
        interval: str,
        aggregation_methods: Optional[Dict[str, str]],
        default_aggregation_method: str
) -> pd.DataFrame:
    if aggregation_methods is None:
        aggregation: Union[str, Dict[str, str]] = default_aggregation_method
    else:
        aggregation = dict(zip(
            df.columns, [default_aggregation_method] * len(df.columns)
        ))
        aggregation.update(aggregation_methods)
    df_resampled = df.resample(interval, on=timestamp_col).agg(aggregation)
    assert isinstance(df_resampled, pd.DataFrame)
    return df_resampled


class Collector:

    def __init__(
            self,
            persistence: PersistenceBase,
            timestamp_col: str
    ) -> None:
        self._persistence = persistence
        self._timestamp_col = timestamp_col

    def save(self, df: pd.DataFrame, timestamp: datetime) -> None:
        if self._timestamp_col not in df.columns:
            raise AssertionError("Timestamp column is missing.")
        self._persistence.save(df, timestamp)

    def get_by_timestamps(
            self,
            earliest_inclusive: datetime,
            latest_exclusive: datetime,
            aggregation_interval: str,
            aggregation_methods: Optional[Dict[str, str]] = None,
            default_aggregation_method: str = "mean"
    ) -> pd.DataFrame:
        df = self._persistence.find_by_timestamps(
            earliest_inclusive, latest_exclusive
        )
        return _resample_df(
            df, self._timestamp_col, aggregation_interval,
            aggregation_methods, default_aggregation_method
        )

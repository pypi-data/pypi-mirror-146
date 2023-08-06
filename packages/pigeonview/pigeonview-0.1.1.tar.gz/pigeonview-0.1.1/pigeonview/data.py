"""
Data utilities.
"""
from datetime import datetime
from typing import Any

import pandas as pd  # type: ignore

from pigeonview.persistence import PersistenceBase


def _resample_df(
        df: pd.DataFrame,
        timestamp_col: str,
        rule: Any,
        dispatching: str
) -> pd.DataFrame:
    df_resampled = getattr(df.resample(rule, on=timestamp_col), dispatching)()
    assert isinstance(df_resampled, pd.DataFrame)
    return df_resampled


class Collector:

    def __init__(
            self,
            persistence: PersistenceBase,
            timestamp_col: str = "_timestamp"
    ) -> None:
        self._persistence = persistence
        self._timestamp_col = timestamp_col

    def save(self, df: pd.DataFrame, timestamp: datetime) -> None:
        if self._timestamp_col not in df.columns:
            raise AssertionError("Timestamp column is missing.")
        self._persistence.save(df, timestamp)

    def get_by_earliest_inclusive(
            self,
            timestamp: datetime,
            rule: Any,
            dispatching: str
    ) -> pd.DataFrame:
        df = self._persistence.find_by_earliest_inclusive(timestamp)
        return _resample_df(df, self._timestamp_col, rule, dispatching)

    def get_by_latest_exclusive(
            self,
            timestamp: datetime,
            rule: Any,
            dispatching: str
    ) -> pd.DataFrame:
        df = self._persistence.find_by_latest_exclusive(timestamp)
        return _resample_df(df, self._timestamp_col, rule, dispatching)

    def close_connection(self) -> None:
        self._persistence.close_connection()

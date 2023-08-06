"""
Persistence utilities.
"""
from abc import ABC
from datetime import datetime, timezone
from typing import Any, Optional, Sequence

import pandas as pd  # type: ignore
import psycopg2  # type: ignore


class PersistenceBase(ABC):

    def save(
            self,
            df: pd.DataFrame,
            timestamp_col: Optional[str],
            timestamp: Optional[datetime]
    ) -> None:
        pass

    def find_by_timestamps(
            self,
            earliest_inclusive: datetime,
            latest_exclusive: Optional[datetime]
    ) -> pd.DataFrame:
        pass

    def close_connection(self) -> None:
        pass


def get_utc_datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class PostgresPersistence(PersistenceBase):
    """
    Table has to be created in advance:

    CREATE TABLE dataframe_record(
        timestamp                     TIMESTAMPTZ PRIMARY KEY NOT NULL,
        dataframe                     VARCHAR NOT NULL
    );
    """

    def __init__(
            self,
            host: str,
            port: str,
            database_name: str,
            user: str,
            password: str
    ) -> None:
        self._conn = psycopg2.connect(
            database=database_name,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def save(
            self,
            df: pd.DataFrame,
            timestamp_col: Optional[str] = None,
            timestamp: Optional[datetime] = None
    ) -> None:
        if timestamp is None:
            timestamp = get_utc_datetime_now()
        if timestamp_col is not None:
            if timestamp_col in df.columns:
                raise ValueError("Timestamp column already exists.")
            df = df.copy()
            df[timestamp_col] = timestamp
        query = "INSERT INTO dataframe_record (timestamp, dataframe) VALUES (%s, %s);"
        params = (timestamp, df.to_json())
        with self._conn:
            with self._conn.cursor() as cursor:
                cursor.execute(query, params)

    def _get_df(self, query: str, params: Sequence[Any]) -> pd.DataFrame:
        with self._conn:
            with self._conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                if not result:
                    return pd.DataFrame()
                df = pd.concat([pd.read_json(row[0]) for row in result])
                return df

    def find_by_timestamps(
            self,
            earliest_inclusive: datetime,
            latest_exclusive: Optional[datetime] = None
    ) -> pd.DataFrame:
        if latest_exclusive is None:
            latest_exclusive = get_utc_datetime_now()
        query = "SELECT dataframe FROM dataframe_record WHERE timestamp >= %s AND timestamp < %s;"
        params = (earliest_inclusive, latest_exclusive)
        return self._get_df(query, params)

    def close_connection(self) -> None:
        self._conn.close()

"""
Persistence utilities.
"""
from abc import ABC
from datetime import datetime
from typing import Any, Sequence

import pandas as pd  # type: ignore
import psycopg2  # type: ignore


class PersistenceBase(ABC):

    def save(self, df: pd.DataFrame, timestamp: datetime) -> None:
        pass

    def find_by_earliest_inclusive(self, timestamp: datetime) -> pd.DataFrame:
        pass

    def find_by_latest_exclusive(self, timestamp: datetime) -> pd.DataFrame:
        pass

    def close_connection(self) -> None:
        pass


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

    def save(self, df: pd.DataFrame, timestamp: datetime) -> None:
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
                df = pd.concat([pd.read_json(row[0]) for row in result])
                return df

    def find_by_earliest_inclusive(self, timestamp: datetime) -> pd.DataFrame:
        query = "SELECT dataframe FROM dataframe_record WHERE timestamp >= %s;"
        params = (timestamp,)
        return self._get_df(query, params)

    def find_by_latest_exclusive(self, timestamp: datetime) -> pd.DataFrame:
        query = "SELECT dataframe FROM dataframe_record WHERE timestamp < %s;"
        params = (timestamp,)
        return self._get_df(query, params)

    def close_connection(self) -> None:
        self._conn.close()

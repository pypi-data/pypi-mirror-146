"""
blink/config.py
Ian Kollipara
2022.03.31

Blink Config
"""

# Imports
from dataclasses import dataclass
from os import getcwd
from typing import List, Literal, Tuple, TypedDict

from .middleware import TulparMiddleware


class SQLiteParams(TypedDict):
    """SQLiteParams denotes the parameters
    needed for an SQLite PonyORM DB Connection.
    """

    filename: str
    create_db: bool


class PostgresParams(TypedDict):
    """PostgresParams denotes the parameters
    needed for an Postgres PonyORM DB Connection.
    """

    user: str
    password: str
    host: str
    database: str


class MySQLParams(TypedDict):
    """MySQLParams denotes the parameters
    needed for an MySQL PonyORM DB Connection.
    """

    user: str
    passwd: str
    host: str
    database: str


class OracleParams(TypedDict):
    """OracleParams denotes the parameters
    needed for an Oracle PonyORM DB Connection.
    """

    user: str
    password: str
    dsn: str


class CockroachParams(TypedDict):
    """CockroachParams denotes the parameters
    needed for an Cockroach PonyORM DB Connection.
    """

    user: str
    passwd: str
    host: str
    database: str
    sslmode: Literal["disable"]


DB_PARAMS = (
    Tuple[Literal["sqlite"], SQLiteParams]
    | Tuple[Literal["postgres"], PostgresParams]
    | Tuple[Literal["mysql"], MySQLParams]
    | Tuple[Literal["oracle"], OracleParams]
    | Tuple[Literal["cockroach"], CockroachParams]
)


@dataclass
class TulparConfig:
    """BlinkConfig is the base class for all configuration files
    `config.py` *must* inherit from this class.
    """

    app_name: str
    db_params: DB_PARAMS
    middleware: List[TulparMiddleware]

    def __call__(self) -> "TulparConfig":
        """Adjust the Config in case of SQLite Database.

        If a SQLite DB is used, adjust the filename to create the db
        in the user directory.
        """

        if (
            self.db_params[0] == "sqlite"
            and self.db_params[1].get("filename", "")[0] != ":"
        ):
            self.db_params[1]["filename"] = f"{getcwd()}/{self.db_params[1].get('filename')}"  # type: ignore

        return self

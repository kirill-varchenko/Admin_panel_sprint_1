import logging
import os
import sqlite3
import sys
import yaml
from dataclasses import dataclass, asdict

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from db_dataclasses import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from db_dataclasses import DATACLASS_TYPES
from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader


@dataclass
class DSN:
    dbname: str
    host: str
    options: str
    password: str
    port: int
    user: str


TABLES_DATACLASSES = [
    ("genre", Genre),
    ("film_work", FilmWork),
    ("person", Person),
    ("genre_film_work", GenreFilmWork),
    ("person_film_work", PersonFilmWork),
]


def load_dsn() -> DSN:
    """Читает параметры подключения к БД Postgres из dsn.yml"""
    try:
        with open("dsn.yml", "r") as fi:
            data = yaml.load(fi, Loader=yaml.Loader)
    except FileNotFoundError:
        logging.exception("File dsn.yml not found.")
        sys.exit(1)

    dsn = DSN(**data)
    return dsn


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    try:
        for data, table in sqlite_loader.load_movies(TABLES_DATACLASSES):
            postgres_saver.save_data(data, table)
    except sqlite3.OperationalError as e:
        logging.exception("Error reading from SQLite.")
    except psycopg2.Error as e:
        logging.exception("Error writing to Postgres.")


if __name__ == "__main__":
    dsn = load_dsn()

    if not os.path.exists("db.sqlite"):
        logging.error('File db.sqlite not found.')
        exit(1)

    try:
        with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
            **asdict(dsn), cursor_factory=DictCursor
        ) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except psycopg2.OperationalError as e:
        logging.exception("Cannot connect to Postgres.")
        exit(1)

    pg_conn.close()
    sqlite_conn.close()

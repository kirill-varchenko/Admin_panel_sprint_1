import logging
import sqlite3
import yaml
from dataclasses import dataclass, asdict

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from db_dataclasses import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork, AbstractRow
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
    with open("dsn.yml", "r") as fi:
        data = yaml.load(fi, Loader=yaml.Loader)
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
        logging.error("Ошибка чтения данных из БД SQLite: %s", e.args[0])
    except psycopg2.Error as e:
        logging.error("Ошибка записи в БД Postgres: %s", e.args[0])


if __name__ == "__main__":
    dsn = load_dsn()

    try:
        with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
            **asdict(dsn), cursor_factory=DictCursor
        ) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except psycopg2.OperationalError as e:
        logging.error("Ошибка подключения к БД Postgres: %s", e.args[0])
    finally:
        pg_conn.close()

    sqlite_conn.close()

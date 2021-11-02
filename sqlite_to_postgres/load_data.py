import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader
from db_dataclasses import Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork

TABLES_DATACLASSES = {
    "genre": Genre,
    "film_work": FilmWork,
    "person": Person,
    "genre_film_work": GenreFilmWork,
    "person_film_work": PersonFilmWork,
}


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    try:
        for data in sqlite_loader.load_movies(TABLES_DATACLASSES):
            postgres_saver.save_all_data(data)
    except sqlite3.OperationalError as e:
        print("Ошибка чтения данных из БД SQLite:", e.args[0])
    except psycopg2.Error as e:
        print("Ошибка записи в БД Postgres:", e.args[0])


if __name__ == "__main__":
    dsl = {
        "dbname": "movies_database",
        "user": "postgres",
        "password": 1234,
        "host": "127.0.0.1",
        "port": 5432,
        "options": "-c search_path=content",
    }
    try:
        with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor
        ) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except psycopg2.OperationalError as e:
        print("Ошибка подключения к БД Postgres:", e.args[0])

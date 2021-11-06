import itertools
import sqlite3


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        """Класс для чтения данных из БД SQLite."""
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.cursor = connection.cursor()

    def load_table(self, table: str, data_class, n: int = 100):
        """Генератор для чтения пачки данных из таблицы."""
        self.cursor.execute(f"SELECT * FROM {table}")
        while True:
            res = [data_class(**item) for item in self.cursor.fetchmany(size=n)]
            if not res:
                return
            yield res

    def load_movies(self, tables_dataclasses: dict, n: int = 100):
        """Генератор для чтения пачек данных из заданных таблиц."""
        table_iters = [self.load_table(table, data_class, n=n) for table, data_class in tables_dataclasses.items()]
        for batch in itertools.chain.from_iterable(table_iters):
            yield batch

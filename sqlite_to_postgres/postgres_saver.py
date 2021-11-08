import re
from dataclasses import astuple
from typing import Optional

from db_dataclasses import DATACLASS_TYPES


class PostgresSaver:
    def __init__(self, connection):
        """Класс для сохранения данных в БД Postgres."""
        self.connection = connection
        self.cursor = self.connection.cursor()

    def make_insert_query(self, data: list[DATACLASS_TYPES], table: str) -> Optional[str]:
        """Метод формирует строку для вставки данных исходя из параметров dataclass.
        Строки, уже существующие в БД, игнорируются."""
        if not data:
            return None
        fields = list(data[0].__dataclass_fields__.keys())
        fields_arg = ", ".join(fields)
        morgify_arg = "(" + ", ".join([r"%s"] * len(fields)) + ")"
        args = ",".join(
            self.cursor.mogrify(morgify_arg, astuple(item)).decode() for item in data
        )
        res = f"""INSERT INTO {table} ({fields_arg})
VALUES {args}
ON CONFLICT (id) DO NOTHING;"""
        return res

    def save_data(self, data: list[DATACLASS_TYPES], table: str) -> None:
        """Метод сохраняет данные в таблицы"""
        if not data:
            return
        insert_query = self.make_insert_query(data, table)
        self.cursor.execute(insert_query)

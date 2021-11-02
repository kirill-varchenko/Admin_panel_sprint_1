import re
from dataclasses import astuple


def camel_to_snake(s: str) -> str:
    """Конвертирует строку из CamelCase в snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


class PostgresSaver:
    def __init__(self, connection):
        """Класс для сохранения данных в БД Postgres."""
        self.connection = connection
        self.cursor = self.connection.cursor()

    def make_insert_query(self, data: list):
        """Метод формирует строку для вставки данных исходя из параметров dataclass.
        Строки, уже существующие в БД, игнорируются."""
        if not data:
            return
        class_name = type(data[0]).__name__
        table_name = camel_to_snake(class_name)
        fields = list(data[0].__dataclass_fields__.keys())
        fields_arg = ", ".join(fields)
        morgify_arg = "(" + ", ".join([r"%s"] * len(fields)) + ")"
        args = ",".join(self.cursor.mogrify(morgify_arg, astuple(item)).decode() for item in data)
        res = f"""INSERT INTO {table_name} ({fields_arg})
VALUES {args}
ON CONFLICT (id) DO NOTHING;"""
        return res

    def save_all_data(self, data):
        """Метод сохраняет данные в таблицы"""
        if not data:
            return
        insert_query = self.make_insert_query(data)
        self.cursor.execute(insert_query)

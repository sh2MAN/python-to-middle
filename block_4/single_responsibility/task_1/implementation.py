import json
from abc import abstractmethod


class AllRecords:
    """Интерфейс для получения записей."""

    @abstractmethod
    def all_records(self):
        """Получение всех записей."""


class Record:
    """Запись."""

    def __init__(self, code, name) -> None:
        super().__init__()
        self.code = code
        self.name = name

    def as_dict(self):
        """Возвращает запись в виде словаря."""
        return {self.code: self.name}


class StoreExporter(AllRecords):
    def to_json(self):
        result = json.dumps([x.as_dict() for x in self.all_records()])

        return result

    def save_to_file(self, path):
        with open(path, 'w') as f:
            f.write(self.to_json())


class RecordStore(StoreExporter, AllRecords):
    """Хранилище записей."""

    def __init__(self) -> None:
        super().__init__()
        self._records = []

    def add_record(self, record: Record):
        """Добавление записи."""
        self._records.append(record)

    def del_record(self, record: Record):
        """Удаление записи."""
        self._records.remove(record)

    def all_records(self) -> list:
        """Возвращает список существующих записей."""
        return self._records

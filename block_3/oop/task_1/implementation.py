import json
from typing import List, Callable, Any, Dict, Union


class Column:
    def __init__(self, name):
        self.name = name
        self.filter = None
        self._visible = True

    @property
    def visible(self):
        return self._visible

    def hide(self):
        self._visible = False

    def show(self):
        self._visible = True


class Row:
    def __init__(self, data: dict):
        self.__dict__.update(data)
        self.fields = data.keys()
        self.select = False


class Table:

    def __init__(self):
        self._columns = {}
        self._column_names = []
        self._rows = []

    def load_row(self, row: dict):
        """Загрузка строки в таблицу."""
        _row = Row(row)
        for col_name in _row.fields:
            if col_name not in self._column_names:
                self._columns[col_name] = Column(col_name)
                self._column_names.append(col_name)
        self._rows.append(_row)

    def load_data(self, data: str):
        """Загрузка данных в таблицу."""
        for row in json.loads(data):
            self.load_row(row)

    def export_row(self, row: Row) -> Dict[str, Any]:
        """Экспортирует строку."""
        obj = {}
        for col_name in self._column_names:
            column = self._columns[col_name]
            if not column.visible:
                continue
            if column.filter and not column.filter(getattr(row, col_name)):
                break
            obj[col_name] = getattr(row, col_name)
        return obj

    def export(self) -> str:
        """Возвращает список данных таблицы."""
        result = []
        for row in self._rows:
            get_row = self.export_row(row)
            if get_row:
                result.append(get_row)
        return json.dumps(result)

    def select_row(self, _id: int):
        """Помечает строку как выбранную."""
        self._select(_id)

    def unselect_row(self, _id: int):
        """Помечает строку как выбранную."""
        self._select(_id, False)

    def _select(self, _id: int, select=True):
        if _id < 0 or _id > len(self._rows):
            assert ValueError('Строка не существует')

        self._rows[_id].select = select

    def delete_selected(self):
        """Удаляет выбранные строки."""
        self._rows = [row for row in self._rows if not row.select]

    def swap_columns(self, l_name, r_name):
        """Поменять колонки местами."""
        if l_name not in self._column_names or r_name not in self._column_names:
            raise ValueError(
                'Передано некорректное наименование одной из колонок'
            )

        c_names = self._column_names
        lid = c_names.index(l_name)
        rid = c_names.index(r_name)
        c_names[lid], c_names[rid] = r_name, l_name

    def hide(self, col_name: str):
        """Скрыть колонку."""
        if col_name not in self._column_names:
            raise ValueError(f'Колонка {col_name} не существует!')

        self._columns[col_name].hide()

    def show(self, col_name: str):
        """Сделать колонку не скрытой."""
        if col_name not in self._column_names:
            raise ValueError(f'Колонка {col_name} не существует!')

        self._columns[col_name].show()

    def set_filter(self, col_name: str, func: Callable[..., Any]):
        """Установка фильтра на колонку.

        Note: В случае если колонка будет скрыта, установленный фильтр не будет
        задействован.
        """
        self._columns[col_name].filter = func

    def set_sorted(self, reverse=False):
        """Сортировка колонок."""
        self._column_names.sort(reverse=reverse)

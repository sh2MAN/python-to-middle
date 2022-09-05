import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course.settings")
django.setup()

from itertools import product
from typing import Union, List, Tuple
from abc import ABC, abstractmethod
from typing import Any
from block_10.explain.task_1.consts import NAMES
from block_10.explain.task_1.models import BookCard, LibraryHall, Librarian, \
    Shelf, Rack, BookStorage
from random import choice, randint


def get_random_name(suffix: str = '', choices: Union[list, tuple] = NAMES) -> str:
    """Получение случайного имени."""
    return f'{choice(choices).title()} {randint(1, 1000)}'


class AbstractProduct(ABC):
    """Абстрактный элемент описывающий создание продукта для библиотеки."""

    @abstractmethod
    def build(self, *args):
        """Создание продукта."""


class AbstractFactory(ABC):

    @abstractmethod
    def create_hall(self) -> AbstractProduct:
        """Создание помещения."""

    @abstractmethod
    def create_shelf(self) -> AbstractProduct:
        """Создание стеллажа."""

    @abstractmethod
    def create_rack(self) -> AbstractProduct:
        """Создание полки."""


class LibraryHallProduct(AbstractProduct):
    """Помещение библиотеки."""

    quantity = 1

    def build(self, librarian: Librarian) -> List[int]:
        """Создание помещения."""
        stor = []

        for _ in range(self.quantity):
            stor.append(
                LibraryHall(
                    name=get_random_name(choices=('зал', 'офис', 'склад', 'холл')),
                    librarian=librarian,
                )
            )
        ids = LibraryHall.objects.bulk_create(stor)
        return ids


class LibraryShelfProduct(AbstractProduct):
    """Стеллаж в помещение."""

    quantity = 5

    def build(self, hall_ids: List[int]) -> List[int]:
        stor = []

        for hall_id in hall_ids:
            for _ in range(self.quantity):
                stor.append(
                    Shelf(
                        name=get_random_name(
                            choices=('стеллаж', 'шкаф')),
                        hall=hall_id,
                    )
                )
        ids = Shelf.objects.bulk_create(stor)
        return ids


class LibraryRackProduct(AbstractProduct):
    """Полка в стеллаж."""

    quantity = 6
    quantity_units = 10

    def build(self, shelf_ids: List[int]) -> Tuple[int, List[int]]:
        stor = []

        for shelf_id in shelf_ids:
            for _ in range(self.quantity):
                stor.append(
                    Rack(
                        name=get_random_name(
                            choices=('полка',)),
                        shelf=shelf_id,
                    )
                )
        ids = Rack.objects.bulk_create(stor)
        return ids, list(range(self.quantity_units))


class LibraryStorageFactory(AbstractFactory):
    """Создает определенные элементы хранилища."""

    def create_hall(self) -> AbstractProduct:
        """Добавление помещения."""
        return LibraryHallProduct()

    def create_shelf(self) -> AbstractProduct:
        """Добавление стеллажа."""
        return LibraryShelfProduct()

    def create_rack(self) -> AbstractProduct:
        """Добавление полок."""
        return LibraryRackProduct()


def create_hall(factory: AbstractFactory, librarian: Librarian):
    hall = factory.create_hall()
    hall_ids = hall.build(librarian)
    shelf = factory.create_shelf()
    shelf_ids = shelf.build(hall_ids)
    rack = factory.create_rack()
    rack_ids = rack.build(shelf_ids)

    stor = []
    for hall_id, shelf_id, rack_id, position_id in product(hall_ids, shelf_ids, *rack_ids):
        stor.append(BookStorage(
            hall=hall_id, shelf=shelf_id, rack=rack_id, position=position_id
        ))
    BookStorage.objects.bulk_create(stor)


class LibraryManager:
    """Менеджер библиотеки.

    Отвечает за поиск новых библиотекарей и помещений.
    """

    def add_hall(self):
        """Добавление помещения."""
        librarian = self.add_librarian()
        create_hall(LibraryStorageFactory(), librarian)

    def add_librarian(self) -> Librarian:
        """Прием нового библиотекаря."""
        return Librarian.objects.create(
            name=get_random_name(choices=NAMES),
        )


class LibrarianManager:
    """Заведующий библиотекой."""

    def add_bookcard(self, book: dict) -> BookCard:
        """Добавление карточки."""
        authors = book.pop('author', None)
        type_publications = book.pop('type_publication', None)
        book_card = BookCard.objects.get_or_create(**book)

        for author in authors:
            book_card.author.get_or_create(short_name=author)

        for type_publication in type_publications:
            book_card.type_publication.get_or_create(name=type_publication)

        book_card.save()

        return book_card


class LibraryWorker:

    def add_book(self, book_card):
        """Добавление книги."""


class LibraryStorage:
    """Хранилище."""

    def __init__(self, manager: LibrarianManager):
        self._storage = []
        self.manager = manager

    def register_book(self, book:dict):
        """Регистрация книги."""
        book_card = self.manager.add_bookcard(book)

#
# if __name__ == '__main__':
#     manager = LibraryManager()
#     manager.add_hall()

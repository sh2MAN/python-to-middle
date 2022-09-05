from typing import Union

from block_10.explain.task_1.consts import NAMES
from block_10.explain.task_1.models import BookCard, LibraryHall, Librarian
from random import choice, randint


def get_random_name(suffix: str = '', choices: Union[list, tuple] = NAMES) -> str:
    """Получение случайного имени."""
    return f'{choice(choices).title} {randint()}'


class Manager:
    """Менеджер."""

    def add_hall(self) -> LibraryHall:
        """Добавление помещения."""
        librarian = self.add_librarian()
        hall = LibraryHall.objects.create(
            name=get_random_name(choices=('зал', 'офис', 'склад', 'холл')),
            librarian=librarian,
        )

        return hall

    def add_librarian(self) -> Librarian:
        """Прием нового библиотекаря."""
        return Librarian.objects.create(
            name=get_random_name(choices=NAMES),
        )


class LibraryStorage:
    """Хранилище."""

    def __init__(self):
        self._storage = []

    def add_book(self, book:dict):
        """Добавление книги в хранилище."""
        book_card = self.add_bookcard(book)

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

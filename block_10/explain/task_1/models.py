from django.db import (
    models, transaction,
)

from block_10.explain.task_1.consts import MAX_BOOK_IN_HALL
from block_10.explain.task_1.errors import TakeBookException


class BookInstanceStatus(models.TextChoices):
    """Статус книги."""

    AVAILABLE = 1, 'Доступна'
    MISSING = 2, 'Отсутствует'


class BookMovementStatus(models.TextChoices):
    """Статус книги в журнале."""

    ISSUED = 1, 'Выдана'
    RETURNED = 2, 'Возвращена'
    MOVEMENT = 3, 'Перемещена'


class Author(models.Model):
    """Автор."""

    short_name = models.CharField(
        'Автор книги',
        max_length=50,
        unique=True,
    )

    class Meta:
        db_table = 'library_author'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class TypePublication(models.Model):
    """Тип издания."""

    name = models.CharField(
        'Тип издания',
        max_length=200,
        unique=True,
    )

    class Meta:
        db_table = 'library_typepublication'
        verbose_name = 'Тип издания'
        verbose_name_plural = 'Типы изданий'


class BookCard(models.Model):
    """Книга."""

    name = models.CharField('Название книги', max_length=100)
    author = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name='Авторы',
    )
    type_publication = models.ManyToManyField(
        TypePublication,
        related_name='type_publications',
        verbose_name='Тип издания',
    )
    isbn = models.CharField(
        'Номер',
        max_length=25,
    )
    number_pages = models.SmallIntegerField('Количество страниц')
    date_publication = models.DateField('Дата публикации')
    description = models.TextField('Описание')

    class Meta:
        db_table = 'library_bookcard'
        verbose_name = 'Книжная карточка'
        verbose_name_plural = 'Книжные карточки'


class Reader(models.Model):
    """Читатель."""

    name = models.CharField(
        'Наименование',
        max_length=50,
    )

    class Meta:
        db_table = 'library_reader'
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class Librarian(models.Model):
    """Библиотекарь."""

    name = models.CharField(
        'Наименование',
        max_length=50,
    )

    class Meta:
        db_table = 'library_librarian'
        verbose_name = "Библиотекарь"
        verbose_name_plural = "Библиотекари"


class ReaderTicket(models.Model):
    """Читательский билет."""

    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        verbose_name='Читатель',
    )
    book = models.ForeignKey(
        BookCard,
        on_delete=models.CASCADE,
        verbose_name='Книга'
    )

    class Meta:
        db_table = 'library_readerticket'
        verbose_name = 'Читательский билет'
        verbose_name_plural = 'Читательские билеты'


class LibraryHall(models.Model):
    """Библиотечный зал."""

    name = models.CharField(
        'Наименование зала',
        max_length=25,
    )
    librarian = models.OneToOneField(
        Librarian,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Закрепленный библиотекарь',
    )

    class Meta:
        db_table = 'library_libraryhall'
        verbose_name = 'Библиотечный зал'
        verbose_name_plural = 'Библиотечные залы'

    @property
    def is_free_space(self):
        return self.books.filter(
            status=BookInstanceStatus.AVAILABLE).count() < MAX_BOOK_IN_HALL


class Shelf(models.Model):
    """Стеллаж."""

    number = models.PositiveSmallIntegerField(
        'Номер стеллажа',
        unique=True
    )
    hall = models.ForeignKey(
        LibraryHall,
        on_delete=models.CASCADE,
        related_name='shelfs',
        verbose_name='Зал',
    )

    class Meta:
        db_table = 'library_shelf'
        verbose_name = 'Стеллаж'
        verbose_name_plural = 'Стеллажи'


class Rack(models.Model):
    """Полка в стеллаже."""

    number = models.PositiveSmallIntegerField(
        'Номер полки',
        unique=True
    )
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.CASCADE,
        related_name='racks',
        verbose_name='Стеллаж',
    )

    class Meta:
        db_table = 'library_rack'
        verbose_name = 'Полка'
        verbose_name_plural = 'Полки'


class BookInstance(models.Model):
    """Книга в библиотеке."""

    book = models.ForeignKey(
        BookCard,
        on_delete=models.CASCADE,
        verbose_name='Карточка',
    )
    status = models.PositiveSmallIntegerField(
        'Статус',
        choices=BookInstanceStatus.choices,
        default=BookInstanceStatus.AVAILABLE,
    )
    hall = models.ForeignKey(
        LibraryHall,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Книжный зал',
        null=True,
    )
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Номер стеллажа',
        null=True,
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Номер полки',
        null=True,
    )

    class Meta:
        db_table = 'library_bookinstance'
        verbose_name = 'Книга в наличии'
        verbose_name_plural = 'Книги в наличии'

    def get_book(self):
        """Получить книгу."""
        if self.status == BookInstanceStatus.MISSING:
            raise TakeBookException('Книгу уже забрали')

        self.take_book(self.pk)

    @classmethod
    def take_book(cls, _id: int) -> 'BookInstance':
        """Выдача книги."""
        with transaction.atomic():
            take_book: BookInstance = cls.objects.select_for_update().get(
                pk=_id)
            take_book.status = BookInstanceStatus.MISSING
            take_book.hall = None
            take_book.shelf = None
            take_book.rack = None
            take_book.save()
            return take_book


class BookMovementLog(models.Model):
    """Журнал перемещения книг."""

    book = models.ForeignKey(
        BookInstance,
        on_delete=models.CASCADE,
        verbose_name='Книга',
    )
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        verbose_name='Читатель',
        null=True,
    )
    librarian = models.ForeignKey(
        Librarian,
        on_delete=models.CASCADE,
        verbose_name='Библиотекарь',
        null=True,
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.RESTRICT,
        verbose_name='Полка',
        null=True,
    )
    date_issue = models.DateField(
        'Дата выдачи книги',
    )
    date_return = models.DateField(
        'Дата возврата книги',
        null=True,
    )
    status = models.PositiveSmallIntegerField(
        'Статус',
        choices=BookMovementStatus.choices,
    )

    class Meta:
        db_table = 'library_bookmovementlog'
        verbose_name = verbose_name_plural = 'Журнал перемещения книг'

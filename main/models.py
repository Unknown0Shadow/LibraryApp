from django.db import models
from datetime import datetime
from .constants import *
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.db.models.signals import post_delete, post_save
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    TITLE = models.CharField(max_length=70, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(category):
        return category.TITLE


class Book(models.Model):
    CATEGORY = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    TITLE = models.CharField(max_length=70, null=False, blank=False)
    DESCRIPTION = models.TextField(null=True, blank=True)
    DATE = models.DateTimeField(default=datetime.now, null=False, blank=False)
    AUTHOR = models.CharField(max_length=50)
    COPIES = models.IntegerField(default=0, null=False, blank=False)
    LANGUAGE = models.CharField(max_length=3,
                                choices=LIST_OF_LANGUAGES,
                                default="ENG")
    PRICE = models.FloatField(default=0.0)
    STATUS = models.CharField(
        max_length=15,
        choices=LIST_OF_STATUSES,
        default="AVAILABLE",
    )

    def get_copies(book):
        copies = [copy for copy in BookCopy.objects.all() if copy.BOOK == book]
        return copies

    def get_success_url(book):
        return reverse("main:home")

    def __str__(book):
        return book.TITLE


class BookCopy(models.Model):
    BOOK = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    LAST_BORROWER = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    LAST_LOANED = models.DateTimeField(default=None, null=True, blank=True)
    CLASSIFICATION = models.CharField(max_length=50, unique=True)
    STATUS = models.CharField(
        max_length=15,
        choices=LIST_OF_STATUSES_COPY,
        default="AVAILABLE"
    )

    class Meta:
        verbose_name = "Copy"
        verbose_name_plural = "Copies"

    def get_success_url(copy):
        return reverse("main:home")

    def get_title(copy):
        return copy.BOOK.TITLE

    def get_author(copy):
        return copy.BOOK.AUTHOR

    def __str__(copy):
        return copy.BOOK.TITLE


def update_bookcopy_count(instance, **kwargs):
    # https://stackoverflow.com/questions/258296/django-models-how-to-filter-number-of-foreignkey-objects/6205303
    if not kwargs.get('created', True) or kwargs.get("raw", False):
        return
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE main_book set COPIES = ('
        'SELECT COUNT(*) FROM main_bookcopy '
        'WHERE main_bookcopy.book_id = main_book.id'
        ') '
        'WHERE id = %s', [instance.BOOK.id])
    transaction.atomic()


def update_sql(status, instance):
    cursor = connection.cursor()
    cursor.execute(
        f'UPDATE main_book set STATUS = "{status}" WHERE id = {instance.id}')
    transaction.atomic()


def update_book_status():
    for book in Book.objects.all():
        copies = [copy for copy in BookCopy.objects.all() if copy.BOOK == book]
        count = 0
        for copy in copies:
            if copy.STATUS == "AVAILABLE":
                count += 1
        # print("Debug -----",book)
        if count == 0:
            update_sql("UNAVAILABLE", book)
        else:
            update_sql("AVAILABLE", book)


def update():
    post_save.connect(update_bookcopy_count, sender=BookCopy)
    post_delete.connect(update_bookcopy_count, sender=BookCopy)
    update_book_status()


update()

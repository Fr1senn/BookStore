from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


def get_full_name(self):
    return f'{self.first_name} {self.last_name}'


User.add_to_class('__str__', get_full_name)


class BaseModel(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=220, verbose_name='URL')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Genre(BaseModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse_lazy('book_by_genre', kwargs={'slug': self.slug})


class Author(models.Model):
    slug = models.SlugField(max_length=220, verbose_name='URL')
    first_name = models.CharField(max_length=220, verbose_name='Имя')
    last_name = models.CharField(max_length=220, verbose_name='Фамилия')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['pk']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse_lazy('book_by_author', kwargs={'slug': self.slug})


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=220, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('book', kwargs={'slug': self.slug})


class Order(models.Model):
    purchase_date = models.DateField(auto_now=True, verbose_name='Дата покупки')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Книга')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['pk']

    def __str__(self):
        return f'{self.user} {self.book}'


class Review(models.Model):
    text = models.TextField(verbose_name='Отзыв')
    writing_date = models.DateTimeField(auto_now=True, verbose_name='Дата написания')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pk']

    def __str__(self):
        return f'{self.user} {self.writing_date}'

from django.contrib import admin

from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug')
    list_display = ('id', 'title')
    list_display_links = ('title',)


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    fields = ('first_name', 'last_name', 'birthday', 'slug')
    list_display = ('id', 'first_name', 'last_name', 'birthday')
    list_filter = ('birthday',)


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'description', 'price', 'genres', 'authors', 'slug')
    list_display = ('id', 'title', 'description', 'price', 'get_genres', 'get_authors')
    list_display_links = ('title',)
    list_filter = ('genres', 'authors', 'price')

    def get_genres(self, obj):
        return ", ".join([item.title for item in obj.genres.all()])

    def get_authors(self, obj):
        return ", ".join([item.last_name for item in obj.authors.all()])


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('text', 'user')
    list_display = ('id', 'user', 'text', 'writing_date')
    list_filter = ('writing_date',)

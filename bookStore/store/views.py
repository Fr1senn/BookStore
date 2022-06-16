from django.contrib.auth.views import LoginView
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.shortcuts import render

from . import models


class HomeView(TemplateView):
    template_name = 'store/index.html'


class ReviewsView(ListView):
    template_name = 'store/reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return models.Review.objects.exclude(user__username='admin')


class CatalogView(ListView):
    template_name = 'store/catalog.html'
    model = models.Book
    context_object_name = 'books'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        context['genres'] = models.Genre.objects.all()
        return context


class BookByAuthorView(CatalogView):
    def get_queryset(self):
        return models.Book.objects.filter(authors__slug=self.kwargs['slug'])


class BookByGenreView(CatalogView):
    def get_queryset(self):
        return models.Book.objects.filter(genres__slug=self.kwargs['slug'])


class BookDetail(DetailView):
    template_name = 'store/book.html'
    model = models.Book
    context_object_name = 'book'


class LoginView(TemplateView):
    template_name = 'store/login.html'

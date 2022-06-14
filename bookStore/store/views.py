from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView

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
    context_object_name = 'books'

    def get_queryset(self):
        return models.Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        context['genres'] = models.Genre.objects.all()
        return context

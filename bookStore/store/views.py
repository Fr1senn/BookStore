from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models
from . import forms


class HomeView(TemplateView):
    template_name = 'store/index.html'


class ReviewsView(ListView):
    template_name = 'store/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 3

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


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LogInView(LoginView):
    template_name = 'registration/login.html'
    form_class = forms.LoginForm

    def get_success_url(self):
        return reverse_lazy('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'store/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = models.Order.objects.filter(user__username=self.request.user.username).order_by('purchase_date')
        return context

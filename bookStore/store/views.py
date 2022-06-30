from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from . import forms, models


class ReviewsView(ListView):
    template_name = 'store/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 3

    def get_queryset(self):
        return models.Review.objects \
            .select_related('user') \
            .exclude(user__username='admin') \
            .values('text', 'writing_date', 'user__first_name', 'user__last_name')


class CatalogView(ListView):
    template_name = 'store/catalog.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return models.Book.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['authors'] = models.Author.objects.all()
        context['genres'] = models.Genre.objects.all()
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = 'store/create_review.html'
    login_url = '/login'
    form_class = forms.ReviewForm
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(CreateReviewView, self).form_valid(form)


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

    def get_queryset(self):
        return models.Book.objects\
            .filter(slug=self.kwargs.get('slug'))\
            .prefetch_related('genres')\
            .prefetch_related('authors')


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
    authentication_form = forms.LoginForm

    def get_success_url(self):
        return reverse_lazy('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'store/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = models.Order.objects \
            .select_related('book') \
            .filter(user__username=self.request.user.username)
        return context


class SearchView(ListView):
    template_name = 'store/search_results.html'
    model = models.Book
    context_object_name = 'books'

    def get_queryset(self):
        return models.Book.objects \
            .filter(title__icontains=self.request.GET.get('search_input'))

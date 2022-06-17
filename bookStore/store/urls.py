from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('book/<slug:slug>/', views.BookDetail.as_view(), name='book'),

    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('catalog/genre/<slug:slug>/', views.BookByGenreView.as_view(), name='book_by_genre'),
    path('catalog/author/<slug:slug>/', views.BookByAuthorView.as_view(), name='book_by_author'),

    path('accounts/registration/', views.RegistrationView.as_view(), name='registration'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),

    path('catalog/', views.CatalogView.as_view(), name='catalog'),
]

from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView


class HomeView(TemplateView):
    template_name = 'store/index.html'

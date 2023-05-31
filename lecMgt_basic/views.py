from django.shortcuts import render
from django.views.generic import ListView, DeleteView, TemplateView, CreateView

# Create your views here.

class HomePage(TemplateView):
    template_name = "frontend/index.html"

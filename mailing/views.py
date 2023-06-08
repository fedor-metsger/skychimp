
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from mailing.models import Client, Task

class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }

class ClientDetailView(DetailView):
    model = Client

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['name', 'email', 'description']

class ClientDeleteView(DeleteView):
    model = Client
class TaskListView(ListView):
    model = Task
    extra_context = {
        'title': 'Рассылки'
    }
    # def get_queryset(self):
    #     queryset = super().get_queryset().order_by('-creation_date')[:5]
    #     return queryset

class TaskDetailView(DetailView):
    model = Task

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'period', 'status', 'subject', 'body']

class TaskDeleteView(DeleteView):
    model = Task



from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.forms import inlineformset_factory

from mailing.models import Client, Task, Interval
from mailing.forms import TaskForm, IntervalForm

class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }

class ClientDetailView(DetailView):
    model = Client

class ClientCreateView(CreateView):
    model = Client
    fields = ['name', 'email', 'description']
    success_url = reverse_lazy("client_list")

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['name', 'email', 'description']
    success_url = reverse_lazy("client_list")

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("client_list")

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

class TaskCreateView(CreateView):
    model = Task
    fields = ["title", "period", "status", "subject", "body"]
    success_url = reverse_lazy("task_list")

class TaskUpdateView(UpdateView):
    model = Task
    fields = ["title", "period", "status", "subject", "body"]
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        IntervalFormSet = inlineformset_factory(Task, Interval, form=IntervalForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = IntervalFormSet(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = IntervalFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("task_list")

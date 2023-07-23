
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max
from django.core.exceptions import PermissionDenied

from blog.models import Article
from crontab.manager import EmailManager
from mailing.models import Client, Task, Interval, Log
from mailing.forms import TaskForm, IntervalForm, ClientForm


# Create your views here.
class ClientListView(UserPassesTestMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }

    def test_func(self):
        return self.request.user.is_authenticated and "manager" not in [i.name for i in self.request.user.groups.all()]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).order_by('pk')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


class ClientDetailView(UserPassesTestMixin, DetailView):
    model = Client

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and (obj.owner_id == self.request.user.id or
                                                       self.request.user.is_superuser)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


class ClientCreateView(UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client_list")

    def test_func(self):
        return self.request.user.is_authenticated and "manager" not in [i.name for i in self.request.user.groups.all()]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        owner_id = self.request.user.id
        kwargs.update({'owner_id': owner_id})
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client_list")

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and (obj.owner_id == self.request.user.id or
                                                       self.request.user.is_superuser)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        owner_id = self.request.user.id
        kwargs.update({'owner_id': owner_id})
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("client_list")

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and (obj.owner_id == self.request.user.id or
                                                       self.request.user.is_superuser)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self):
        if "manager" in [i.name for i in self.request.user.groups.all()]:
            return super().get_queryset()
        return super().get_queryset().filter(owner=self.request.user).order_by('pk')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


class TaskDetailView(UserPassesTestMixin, DetailView):
    model = Task

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and (
                obj.owner_id == self.request.user.id or
                "manager" in [i.name for i in self.request.user.groups.all()] or
                self.request.user.is_superuser)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        obj = self.get_object()
        if obj.status == Task.RUNNING:
            context_data["button_text"] = "Остановить"
        else:
            context_data["button_text"] = "Запустить"

        return context_data


class TaskCreateView(UserPassesTestMixin, CreateView):
    model = Task
    fields = ["title", "period", "status", "subject", "body"]
    success_url = reverse_lazy("task_list")

    def test_func(self):
        return self.request.user.is_authenticated and "manager" not in [i.name for i in self.request.user.groups.all()]

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        IntervalFormSet = inlineformset_factory(Task, Interval, form=IntervalForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = IntervalFormSet(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = IntervalFormSet(instance=self.object)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        if form.is_valid():
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)


class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["title", "period", "status", "subject", "body"]
    success_url = reverse_lazy("task_list")

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and (obj.owner_id == self.request.user.id or
                                                       self.request.user.is_superuser)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        IntervalFormSet = inlineformset_factory(Task, Interval, form=IntervalForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = IntervalFormSet(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = IntervalFormSet(instance=self.object)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task_list")

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and (obj.owner_id == self.request.user.id or
                                                       self.request.user.is_superuser)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
        return context_data


# @cache_page(3)
def index_view(request):
    tasks = Task.objects.count()
    active = Task.objects.filter(status=Task.RUNNING).count()
    clients = Client.objects.count()
    articles = Article.objects.order_by('?')[0:3]
    crontab_status = "Запущен" if EmailManager.crontab_status else "Остановлен"
    context = {
        "not_manager": "manager" not in [i.name for i in request.user.groups.all()],
        "tasks": tasks,
        "active": active,
        "clients": clients,
        "articles": articles,
        "crontab_status": crontab_status
    }
    return render(request, "mailing/index.html", context=context)


def switch_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.user.is_authenticated and (
            task.owner_id == request.user.id or
            "manager" in [i.name for i in request.user.groups.all()] or
            request.user.is_superuser):
        if task.status == Task.RUNNING:
            task.status = Task.FINISHED
        else:
            task.status = Task.RUNNING
        task.save()
    return redirect(f'/task/{pk}/')


def tasks_report(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        raise PermissionDenied()

    tasks = Log.objects.values("task", "client").annotate(
        last_run=Max("time")
    ).order_by("task", "client")

    for t in tasks:
        t["task_title"] = Task.objects.get(pk=t["task"])
        t["client_name"] = Client.objects.get(pk=t["client"])

    context = {
        "not_manager": "manager" not in [i.name for i in request.user.groups.all()],
        "tasks": tasks
    }
    return render(request, "mailing/report.html", context=context)

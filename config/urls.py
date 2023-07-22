"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from mailing.crontab import EmailManager
from mailing.views import TaskDetailView, TaskListView, TaskUpdateView, TaskDeleteView, TaskCreateView, index_view, \
    tasks_report
from mailing.views import switch_task
from mailing.views import ClientListView, ClientDetailView, ClientDeleteView, ClientUpdateView, ClientCreateView

# app_name = 'catalog'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index_view, name='index'),
    path('report/', tasks_report, name='report'),
    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/switch/', switch_task, name='task_switch'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('send/', EmailManager.send_emails, name='switch_crontab'),
    path('crontab/', EmailManager.switch_crontab, name='switch_crontab'),

    path('user/', include('users.urls', namespace='user')),
    path('blog/', include('blog.urls', namespace='blog'))
]
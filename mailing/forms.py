
from  django import forms

from mailing.models import Task, Interval

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class IntervalForm(forms.ModelForm):
    class Meta:
        model = Interval
        fields = "__all__"

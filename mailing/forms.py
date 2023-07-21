
from  django import forms

from mailing.models import Task, Interval, Client


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class IntervalForm(forms.ModelForm):
    class Meta:
        model = Interval
        fields = "__all__"

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)

    def __init__(self, owner_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tasks"].queryset = self.fields["tasks"].queryset.filter(owner_id=owner_id)
        for field_name, field in self.fields.items():
            print()

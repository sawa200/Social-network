from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "location", "start", "end", "all_day", "creator"]
        widgets = {
            "start": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "description": forms.Textarea(attrs={"rows":3}),
        }

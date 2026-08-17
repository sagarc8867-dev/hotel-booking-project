from django import forms
from .models import Housekeeping

class HousekeepingForm(forms.ModelForm):

    class Meta:
        model = Housekeeping
        fields = "__all__"

        widgets = {

            "room": forms.Select(attrs={
                "class":"form-control"
            }),

            "staff_name": forms.TextInput(attrs={
                "class":"form-control"
            }),

            "status": forms.Select(attrs={
                "class":"form-control"
            }),

            "remarks": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4
            }),

        }
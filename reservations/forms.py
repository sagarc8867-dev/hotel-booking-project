from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = "__all__"

        widgets = {

            "guest": forms.Select(attrs={"class":"form-control"}),

            "room": forms.Select(attrs={"class":"form-control"}),

            "check_in": forms.DateInput(attrs={
                "type":"date",
                "class":"form-control"
            }),

            "check_out": forms.DateInput(attrs={
                "type":"date",
                "class":"form-control"
            }),

            "number_of_guests": forms.NumberInput(attrs={
                "class":"form-control"
            }),

            "status": forms.Select(attrs={
                "class":"form-control"
            }),

        }
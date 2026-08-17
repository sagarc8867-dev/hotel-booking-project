from django import forms
from django.utils import timezone
from .models import Room, RoomType
from hotels.forms import CommaSeparatedListField


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = "__all__"

        widgets = {
            "hotel": forms.Select(attrs={"class": "form-control"}),
            "room_type": forms.Select(attrs={"class": "form-control"}),
            "room_number": forms.TextInput(attrs={"class": "form-control"}),
            "floor": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "price_override": forms.NumberInput(attrs={"class": "form-control"}),
        }


class RoomSearchForm(forms.Form):

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "City"
        })
    )

    check_in = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
            "min": timezone.now().date().isoformat(),
        })
    )

    check_out = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
            "min": timezone.now().date().isoformat(),
        })
    )

    guests = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Guests"
        })
    )

class RoomTypeForm(forms.ModelForm):

    amenities = CommaSeparatedListField(
        required=False,
        label="Amenities",
        help_text="Separate each amenity with a comma — no brackets or quotes needed.",
    )

    class Meta:
        model = RoomType
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "base_price": forms.NumberInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
        }
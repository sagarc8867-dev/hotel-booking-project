from django import forms
from .models import Hotel


class CommaSeparatedListField(forms.Field):
    """Lets staff type a plain comma-separated list (e.g. 'Free WiFi, Pool, Spa')
    instead of hand-writing JSON. Stored on the model's JSONField as a list."""

    widget = forms.Textarea(attrs={
        "class": "form-control",
        "rows": 3,
        "placeholder": "Comma-separated, e.g. Free WiFi, Swimming Pool, Spa, Parking",
    })

    def prepare_value(self, value):
        if isinstance(value, (list, tuple)):
            return ", ".join(str(v) for v in value)
        return value or ""

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in str(value).split(",") if item.strip()]

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        return value


class HotelForm(forms.ModelForm):

    amenities = CommaSeparatedListField(
        required=False,
        label="Amenities",
        help_text="Separate each amenity with a comma — no brackets or quotes needed.",
    )

    class Meta:
        model = Hotel
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "city": forms.TextInput(attrs={"class":"form-control"}),
            "state": forms.TextInput(attrs={"class":"form-control"}),
            "address": forms.Textarea(attrs={"class":"form-control","rows":3}),
            "star_rating": forms.NumberInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control","rows":4}),
        }

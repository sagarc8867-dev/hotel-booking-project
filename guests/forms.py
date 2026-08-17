import re
from django import forms
from .models import Guest

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'phone', 'age',
                   'id_proof_type', 'id_proof_number', 'address']

        widgets = {
            "first_name": forms.TextInput(attrs={"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 18, "max": 120}),
            "address": forms.Textarea(attrs={"class":"form-control","rows":3}),
            "id_proof_type": forms.Select(attrs={"class":"form-control"}),
            "id_proof_number": forms.TextInput(attrs={"class":"form-control"}),
        }

    ID_PROOF_PATTERNS = {
        "aadhar": (r"^\d{12}$", "Aadhar number must be exactly 12 digits."),
        "pan": (r"^[A-Z]{5}[0-9]{4}[A-Z]$", "PAN must be in the format ABCDE1234F."),
        "passport": (r"^[A-Z][0-9]{7}$", "Passport number must be 1 letter followed by 7 digits, e.g. A1234567."),
        "driving_license": (r"^[A-Z0-9]{10,16}$", "Driving License must be 10–16 letters/numbers."),
        "voter_id": (r"^[A-Z]{3}[0-9]{7}$", "Voter ID must be 3 letters followed by 7 digits, e.g. ABC1234567."),
    }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise forms.ValidationError("Guests must be 18 or older to book a room.")
        return age

    def clean(self):
        cleaned_data = super().clean()
        id_type = cleaned_data.get("id_proof_type")
        id_number = cleaned_data.get("id_proof_number")

        if id_type and id_number:
            id_number = id_number.strip().upper()
            pattern, error_message = self.ID_PROOF_PATTERNS.get(id_type, (None, None))
            if pattern and not re.match(pattern, id_number):
                self.add_error("id_proof_number", error_message)
            else:
                cleaned_data["id_proof_number"] = id_number

        return cleaned_data
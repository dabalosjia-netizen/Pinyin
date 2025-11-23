from django import forms
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_configs = {
            "username": {"placeholder": "Create a username", "autocomplete": "username"},
            "email": {"placeholder": "you@example.com", "autocomplete": "email"},
            "password1": {"placeholder": "Choose a secure password", "autocomplete": "new-password"},
            "password2": {"placeholder": "Repeat password", "autocomplete": "new-password"},
        }

        for name, field in self.fields.items():
            config = field_configs.get(name, {})
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs.update(
                {
                    "class": f"input {classes}".strip(),
                    **config,
                }
            )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'price', 'image']
        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter barcode'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

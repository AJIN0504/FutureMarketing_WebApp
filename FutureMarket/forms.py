# from django import forms
# from . models import RegisterViewModel
# import re

# class RequestViewForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = RegisterViewModel
#         fields = "__all__"

#     # Must be lowercase 'clean_'
#     def clean_supplyername(self):
#         supplyername = self.cleaned_data["supplyername"]
#         if len(supplyername) < 1:
#             raise forms.ValidationError("Please enter a valid name")
#         return supplyername


#     def clean_password(self):
#         password = self.cleaned_data["password"]
#         if not re.search(r'[A-Z]',password):
#                 raise forms.ValidationError("Password should contain a uppercase charecter")
#         if not re.search(r'[a-z]',password):
#                         raise forms.ValidationError("Password should contain a  lowercase charecter")
#         if not re.search(r'[0-9]',password):
#                     raise forms.ValidationError("Password should contain an integer")
#         if not re.search(r'[@^/$&*]',password):
#                     raise forms.ValidationError("Password should contain a special charecter")
        
#         return password

#     def clean(self):
#         data=super().clean()
#         password=data.get("password")
#         confirm_password=data.get("confirm_password")
#         if password and confirm_password:
#             if password != confirm_password:
#                 self.add_error("confirm_password","password and comfirm password mismatch")
#         return data


from django import forms
from django.contrib.auth.hashers import make_password
from .models import QuoteRequest, Review, Supplier
import re


class SupplierRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Create a strong password"}),
        help_text="Min 8 characters with uppercase, lowercase, a number and a special character.",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password"})
    )

    class Meta:
        model = Supplier
        # Explicit list instead of "__all__" so created_at etc. never leak into the form
        fields = ["fullname", "company_name", "email", "phone", "address", "password"]
        labels = {"fullname": "Supplier name", "company_name": "Company / shop name"}
        widgets = {
            "fullname": forms.TextInput(attrs={"placeholder": "Enter supplier name"}),
            "company_name": forms.TextInput(attrs={"placeholder": "Optional"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 XXXXXXXXXX"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Business address"}),
        }

    def clean_fullname(self):
        name = self.cleaned_data["fullname"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter a valid name.")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Supplier.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A supplier with this email is already registered.")
        return email

    def clean_phone(self):
        # Remove spaces/dashes so "+91 96337-79978" passes the validator
        return re.sub(r"[\s\-]", "", self.cleaned_data["phone"])

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password should contain an uppercase character.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Password should contain a lowercase character.")
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password should contain a number.")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise forms.ValidationError("Password should contain a special character.")
        return password

    def clean(self):
        data = super().clean()
        password = data.get("password")
        confirm = data.get("confirm_password")
        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Password and confirm password do not match.")
        return data

    def save(self, commit=True):
        supplier = super().save(commit=False)
        supplier.password = make_password(self.cleaned_data["password"])  # hash it
        if commit:
            supplier.save()
        return supplier


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]
        labels = {"name": "Your name", "comment": "Your review"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "comment": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Tell us about the quality, fit and delivery..."}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your name.")
        return name

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()
        if len(comment) < 10:
            raise forms.ValidationError("Please write at least 10 characters.")
        return comment


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ["name", "organisation", "email", "phone", "category", "quantity", "message"]
        labels = {
            "name": "Your name",
            "organisation": "School / college / hospital / company",
            "category": "What do you need?",
            "quantity": "Approximate quantity",
            "message": "Details",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "organisation": forms.TextInput(attrs={"placeholder": "Optional"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 XXXXXXXXXX"}),
            "quantity": forms.NumberInput(attrs={"min": 1, "placeholder": "e.g. 250"}),
            "message": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Sizes, colours, fabric, delivery date..."}
            ),
        }

    def clean_phone(self):
        return re.sub(r"[\s\-]", "", self.cleaned_data["phone"])
    
# from django.db import models

# # Create your models here.
# class RegisterViewModel(models.Model):
#     fullname = models.CharField(max_length= 50)
#     username = models.CharField(max_length= 50)
#     email = models.EmailField()
#     password = models.CharField(max_length= 50)
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

phone_validator = RegexValidator(
    r"^\+?\d{10,13}$", "Enter a valid phone number (10-13 digits, optional leading +)."
)


class Supplier(models.Model):
    fullname = models.CharField("Supplier name", max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[phone_validator])
    address = models.TextField(blank=True)
    # Stores the HASHED password (make_password output is ~100 chars), never plain text
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.fullname} <{self.email}>"


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)]

    name = models.CharField(max_length=60)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(max_length=1000)
    approved = models.BooleanField(default=True)  # untick in admin to hide a review
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


class QuoteRequest(models.Model):
    CATEGORY_CHOICES = [
        ("school", "School uniforms"),
        ("college", "College uniforms"),
        ("hospital", "Hospital uniforms"),
        ("kitex", "Kitex products / distribution"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=60)
    organisation = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, validators=[phone_validator])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"
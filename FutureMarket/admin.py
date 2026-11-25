from django.contrib import admin

from .models import QuoteRequest, Review, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("fullname", "company_name", "email", "phone", "created_at")
    search_fields = ("fullname", "company_name", "email")
    exclude = ("password",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "approved", "created_at")
    list_filter = ("approved", "rating")
    list_editable = ("approved",)


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "category", "quantity", "phone", "created_at")
    list_filter = ("category",)
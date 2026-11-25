from django.urls import path
from FutureMarket import views

urlpatterns = [
    path("", views.welcomepage, name="welcome"),
    path("supplier-register/", views.supplier_register, name="supplier_register"),
    path("reviews/", views.reviews, name="reviews"),
    path("request-quote/", views.request_quote, name="request_quote"),
]